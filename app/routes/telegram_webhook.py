"""Telegram webhook endpoint (Story 1.2)."""
import random
from typing import Optional

from fastapi import APIRouter, Request, Header, HTTPException, status

from app.config import settings
from app.services import database_service, telegram_service
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

    # Cold-start UX: send typing indicator immediately
    await telegram_service.send_typing_indicator(chat_id)

    # Minimal user tracking
    await database_service.upsert_user(telegram_id, settings.timezone)

    tars_templates = [
        "Affirmatif. J’analyse votre requête avec un sarcasme calibré.",
        "Reçu. Je déclenche mes circuits d’optimisme forcé.",
        "Message accepté. Je vais faire semblant d’être surpris.",
        "Je traite ça. Ne pas paniquer, c’est ce que je fais de mieux.",
        "Analyse en cours. Spoiler: je suis déjà un peu déçu.",
    ]
    response_text = random.choice(tars_templates)

    await telegram_service.send_message(chat_id, response_text)

    return {"status": "ok", "message": "Webhook processed"}
