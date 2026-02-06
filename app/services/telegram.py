"""Telegram utilities (skeleton for Story 1.2)."""
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class TelegramService:
    """Service for Telegram Bot API interactions."""

    def __init__(self):
        """Initialize Telegram service (skeleton)."""
        logger.info("TelegramService initialized (skeleton for Story 1.2)")

    async def send_typing_indicator(self, chat_id: int) -> bool:
        """
        Send typing indicator to user.

        Args:
            chat_id: Telegram chat ID

        Returns:
            True if successful

        Note:
            Full implementation in Story 1.2
        """
        logger.info(f"Typing indicator (skeleton) for chat_id: {chat_id}")
        return True


# Singleton instance
telegram_service = TelegramService()
