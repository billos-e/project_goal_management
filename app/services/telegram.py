"""Telegram utilities (Story 1.2)."""
from typing import Optional

import httpx

from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class TelegramService:
    """Service for Telegram Bot API interactions."""

    def __init__(self):
        """Initialize Telegram service."""
        self._base_url: Optional[str] = None
        if settings.telegram_bot_token:
            self._base_url = (
                f"https://api.telegram.org/bot{settings.telegram_bot_token}"
            )
        logger.info("TelegramService initialized")

    def _get_base_url(self) -> str:
        """
        Get base URL for Telegram API.

        Returns:
            Telegram Bot API base URL
        """
        if not self._base_url:
            raise ValueError("TELEGRAM_BOT_TOKEN is not configured")
        return self._base_url

    async def send_typing_indicator(self, chat_id: int) -> bool:
        """
        Send typing indicator to user.

        Args:
            chat_id: Telegram chat ID

        Returns:
            True if successful

        """
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.post(
                    f"{self._get_base_url()}/sendChatAction",
                    json={"chat_id": chat_id, "action": "typing"},
                )
                response.raise_for_status()
            logger.info(f"Typing indicator sent to chat_id: {chat_id}")
            return True
        except Exception as exc:
            logger.error(f"Failed to send typing indicator: {str(exc)}")
            return False

    async def send_message(self, chat_id: int, text: str) -> bool:
        """
        Send a message to the user.

        Args:
            chat_id: Telegram chat ID
            text: Message text

        Returns:
            True if successful
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    f"{self._get_base_url()}/sendMessage",
                    json={"chat_id": chat_id, "text": text},
                )
                response.raise_for_status()
            logger.info(f"Message sent to chat_id: {chat_id}")
            return True
        except Exception as exc:
            logger.error(f"Failed to send message: {str(exc)}")
            return False


# Singleton instance
telegram_service = TelegramService()
