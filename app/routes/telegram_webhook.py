"""Telegram webhook endpoint (skeleton for Story 1.2)."""
from fastapi import APIRouter, Request, Header, HTTPException, status
from typing import Optional
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
    Telegram webhook endpoint (skeleton).

    Args:
        bot_token: Bot token from URL path
        request: FastAPI request object
        x_telegram_bot_api_secret_token: Secret token header

    Returns:
        Acknowledgment response

    Note:
        Full implementation with NLU processing in Story 1.3
        Full authentication validation in Story 1.2
    """
    # Log incoming webhook
    body = await request.json()
    logger.info(
        "Telegram webhook received (skeleton)",
        extra={
            "bot_token": bot_token[:10] + "...",  # Log partial for security
            "has_secret": x_telegram_bot_api_secret_token is not None,
            "update_id": body.get("update_id")
        }
    )

    # Skeleton: Just acknowledge receipt
    # Story 1.2 will add proper authentication
    # Story 1.3 will add NLU processing

    return {"status": "ok", "message": "Webhook received (skeleton)"}
