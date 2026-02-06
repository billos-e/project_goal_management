"""Telegram webhook endpoint (Stories 1.2-1.4)."""
from typing import Optional

from fastapi import APIRouter, Request, Header, HTTPException, status

from app.config import settings
from app.services import (
    database_service,
    habit_service,
    nlu_service,
    objective_service,
    telegram_service,
)
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/webhook/{bot_token}", status_code=status.HTTP_200_OK)
async def telegram_webhook(
    bot_token: str,
    request: Request,
    x_telegram_bot_api_secret_token: Optional[str] = Header(None)
) -> dict:
    """
    Telegram webhook endpoint.

    Args:
        bot_token: Bot token from URL path
        request: FastAPI request object
        x_telegram_bot_api_secret_token: Secret token header

    Returns:
        Acknowledgment response

    """
    if not settings.telegram_webhook_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook secret is not configured",
        )

    if x_telegram_bot_api_secret_token != settings.telegram_webhook_secret:
        logger.warning(
            "Invalid Telegram secret token",
            extra={"has_secret": x_telegram_bot_api_secret_token is not None},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid secret token",
        )

    if settings.telegram_bot_token and bot_token != settings.telegram_bot_token:
        logger.warning("Invalid bot token in webhook path")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid bot token",
        )

    body = await request.json()
    logger.info(
        "Telegram webhook received",
        extra={
            "bot_token": bot_token[:10] + "...",
            "update_id": body.get("update_id"),
        },
    )

    message = body.get("message") or body.get("edited_message")
    if not message:
        return {"status": "ok", "message": "No message to process"}

    chat = message.get("chat", {})
    sender = message.get("from", {})
    chat_id = chat.get("id")
    telegram_id = sender.get("id")

    if chat_id is None or telegram_id is None:
        return {"status": "ok", "message": "Missing chat or user info"}

    text = message.get("text", "")

    # Cold-start UX: send typing indicator immediately
    await telegram_service.send_typing_indicator(chat_id)

    # Minimal user tracking
    await database_service.upsert_user(telegram_id, settings.timezone)

    normalized_text = text.strip()
    lowered_text = normalized_text.lower()

    if lowered_text.startswith("/self_test"):
        db_ok = await database_service.health_check()
        gemini_ok, gemini_error = await nlu_service.health_check()

        response_lines = [
            "🔎 Diagnostic système",
            f"DB: {'✅' if db_ok else '❌'}",
            f"Gemini: {'✅' if gemini_ok else '❌'}",
        ]
        if not gemini_ok and gemini_error:
            response_lines.append(f"Gemini error: {gemini_error}")

        response_text = "\n".join(response_lines)
        await telegram_service.send_message(chat_id, response_text)
        return {"status": "ok", "message": "Self-test processed"}

    if lowered_text.startswith("new habit:"):
        raw_habit = normalized_text.split(":", 1)[1].strip()
        created, response_text = await habit_service.create_habit(telegram_id, raw_habit)
        await telegram_service.send_message(chat_id, response_text)
        return {
            "status": "ok",
            "message": "Habit created" if created else "Habit creation failed",
        }

    if lowered_text.startswith("new goal:"):
        raw_goal = normalized_text.split(":", 1)[1].strip()
        created, response_text = await objective_service.create_objective(telegram_id, raw_goal)
        await telegram_service.send_message(chat_id, response_text)
        return {
            "status": "ok",
            "message": "Objective created" if created else "Objective creation failed",
        }

    if lowered_text.startswith((
        "show habits",
        "list habits",
        "mes habitudes",
        "liste habitudes",
        "voir habitudes",
    )):
        habits = await habit_service.list_habits(telegram_id)
        response_text = habit_service.format_habit_list(habits)
        await telegram_service.send_message(chat_id, response_text)
        return {"status": "ok", "message": "Habits listed"}

    if lowered_text.startswith((
        "show goals",
        "list goals",
        "mes objectifs",
        "liste objectifs",
        "voir objectifs",
    )):
        objectives = await objective_service.list_objectives(telegram_id)
        user_timezone = await objective_service.get_user_timezone(telegram_id)
        response_text = objective_service.format_objective_list(objectives, user_timezone)
        await telegram_service.send_message(chat_id, response_text)
        return {"status": "ok", "message": "Objectives listed"}
    nlu_result = await nlu_service.identify_intent(text)
    response_text = nlu_result.get("response_text") or "Réponse indisponible."

    await telegram_service.send_message(chat_id, response_text)

    return {"status": "ok", "message": "Webhook processed"}
