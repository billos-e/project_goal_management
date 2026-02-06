"""Database service for Supabase connection and queries."""
from typing import Any, Dict, List, Optional
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

    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user record by Telegram ID.

        Args:
            telegram_id: Telegram user ID

        Returns:
            User record dict if found, else None
        """
        try:
            client = self.get_client()
            result = (
                client.table("users")
                .select("*")
                .eq("telegram_id", telegram_id)
                .limit(1)
                .execute()
            )
            if result.data:
                return result.data[0]
            return None
        except Exception as exc:
            logger.error(f"Failed to fetch user: {str(exc)}")
            return None

    async def create_habit(
        self,
        user_id: str,
        title: str,
        frequency_type: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Create a habit record.

        Args:
            user_id: User UUID
            title: Habit title
            frequency_type: daily|weekly|custom

        Returns:
            Created habit record dict if successful, else None
        """
        try:
            client = self.get_client()
            payload = {
                "user_id": user_id,
                "title": title,
                "frequency_type": frequency_type,
            }
            result = client.table("habits").insert(payload).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as exc:
            logger.error(f"Failed to create habit: {str(exc)}")
            return None

    async def create_habit_schedules(
        self,
        habit_id: str,
        schedules: List[Dict[str, Any]],
    ) -> bool:
        """
        Create habit schedule records.

        Args:
            habit_id: Habit UUID
            schedules: List of schedule dicts with day_of_week/time_of_day

        Returns:
            True if successful
        """
        if not schedules:
            return True

        try:
            client = self.get_client()
            payload = [
                {
                    "habit_id": habit_id,
                    "day_of_week": schedule.get("day_of_week"),
                    "time_of_day": schedule.get("time_of_day"),
                }
                for schedule in schedules
            ]
            client.table("habit_schedules").insert(payload).execute()
            return True
        except Exception as exc:
            logger.error(f"Failed to create habit schedules: {str(exc)}")
            return False

    async def delete_habit(self, habit_id: str) -> bool:
        """
        Delete a habit by id.

        Args:
            habit_id: Habit UUID

        Returns:
            True if successful
        """
        try:
            client = self.get_client()
            client.table("habits").delete().eq("id", habit_id).execute()
            return True
        except Exception as exc:
            logger.error(f"Failed to delete habit: {str(exc)}")
            return False

    async def list_habits(self, user_id: str) -> List[Dict[str, Any]]:
        """
        List active habits for a user.

        Args:
            user_id: User UUID

        Returns:
            List of habit records
        """
        try:
            client = self.get_client()
            result = (
                client.table("habits")
                .select("*")
                .eq("user_id", user_id)
                .eq("active", True)
                .order("created_at", desc=False)
                .execute()
            )
            return result.data or []
        except Exception as exc:
            logger.error(f"Failed to list habits: {str(exc)}")
            return []

# Singleton instance
database_service = DatabaseService()
