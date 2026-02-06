"""Database service for Supabase connection and queries."""
from typing import Optional
from supabase import create_client, Client
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class DatabaseService:
    """Service for managing Supabase database connections."""

    def __init__(self):
        """Initialize Supabase client."""
        self._client: Optional[Client] = None

    def get_client(self) -> Client:
        """
        Get or create Supabase client instance.

        Returns:
            Supabase client
        """
        if self._client is None:
            try:
                self._client = create_client(
                    settings.supabase_url,
                    settings.supabase_key
                )
                logger.info("Supabase client initialized successfully")
            except Exception as exc:
                logger.error(f"Failed to initialize Supabase client: {str(exc)}")
                raise

        return self._client

    async def health_check(self) -> bool:
        """
        Validate database connection.

        Returns:
            True if connection is healthy, False otherwise
        """
        try:
            client = self.get_client()
            
            # Simple query to verify connection
            # Query the _system_health table or a simple system query
            result = client.table("_system_health").select("*").limit(1).execute()
            
            logger.info("Database health check passed")
            return True

        except Exception as exc:
            logger.error(f"Database health check failed: {str(exc)}")
            return False

    async def upsert_user(self, telegram_id: int, timezone: str) -> bool:
        """
        Insert or update a user record.

        Args:
            telegram_id: Telegram user ID
            timezone: User timezone

        Returns:
            True if successful
        """
        try:
            client = self.get_client()
            payload = {"telegram_id": telegram_id, "timezone": timezone}
            client.table("users").upsert(payload).execute()
            logger.info(f"User upserted: {telegram_id}")
            return True
        except Exception as exc:
            logger.error(f"Failed to upsert user: {str(exc)}")
            return False


# Singleton instance
database_service = DatabaseService()
