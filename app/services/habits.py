"""Habit service for creation and listing."""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from app.config import settings
from app.services.database import database_service
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

FREQUENCY_DAILY = "daily"
FREQUENCY_WEEKLY = "weekly"
FREQUENCY_CUSTOM = "custom"

DAY_MAP = {
    "monday": 0,
    "lundi": 0,
    "tuesday": 1,
    "mardi": 1,
    "wednesday": 2,
    "mercredi": 2,
    "thursday": 3,
    "jeudi": 3,
    "friday": 4,
    "vendredi": 4,
    "saturday": 5,
    "samedi": 5,
    "sunday": 6,
    "dimanche": 6,
}


class HabitService:
    """Service layer for habit operations."""

    def __init__(self) -> None:
        self._database = database_service

    async def create_habit(self, telegram_id: int, raw_text: str) -> Tuple[bool, str]:
        """
        Create a habit from a raw user command text.

        Args:
            telegram_id: Telegram user ID
            raw_text: Habit description from user

        Returns:
            Tuple[bool, str]: (success, response_text)
        """
        title = raw_text.strip()
        if not title:
            return False, "Je ne vois pas d’habitude à créer. Reformule, humain."

        user = await self._get_or_create_user(telegram_id)
        if not user:
            return False, "Impossible d’identifier l’utilisateur. Diagnostic conseillé."

        frequency_type = self._infer_frequency_type(title)
        day_of_week = self._extract_days(title)
        if frequency_type == FREQUENCY_WEEKLY and not day_of_week:
            frequency_type = FREQUENCY_DAILY

        time_of_day = self._normalize_time(
            self._extract_time(title) or user.get("notification_start") or "06:00"
        )

        schedules = self._build_schedules(frequency_type, day_of_week, time_of_day)
        habit = await self._database.create_habit(
            user_id=str(user.get("id")),
            title=title,
            frequency_type=frequency_type,
        )
        if not habit:
            return False, "Création échouée. Mes circuits refusent de coopérer."

        created = await self._database.create_habit_schedules(
            habit_id=str(habit.get("id")),
            schedules=schedules,
        )
        if not created:
            await self._database.delete_habit(str(habit.get("id")))
            return False, "Habitude créée puis annulée. Schedule incomplète."

        response_text = (
            "Habitude enregistrée. Tu persistes, je surveille.\n"
            f"• {title}\n"
            f"• Fréquence: {frequency_type}"
        )
        return True, response_text

    async def list_habits(self, telegram_id: int) -> List[Dict[str, Any]]:
        """
        List active habits for a telegram user.

        Args:
            telegram_id: Telegram user ID

        Returns:
            List of habit records
        """
        user = await self._database.get_user_by_telegram_id(telegram_id)
        if not user:
            return []
        return await self._database.list_habits(str(user.get("id")))

    def format_habit_list(self, habits: List[Dict[str, Any]]) -> str:
        """
        Format habit listing message.

        Args:
            habits: List of habit records

        Returns:
            Formatted response text
        """
        if not habits:
            return "Aucune habitude enregistrée. C’est vide, comme l’espace."

        lines = ["Vos habitudes :"]
        for index, habit in enumerate(habits, start=1):
            title = habit.get("title") or "(sans titre)"
            frequency = habit.get("frequency_type") or "daily"
            lines.append(f"{index}. {title} — {frequency}")
        return "\n".join(lines)

    async def _get_or_create_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        user = await self._database.get_user_by_telegram_id(telegram_id)
        if user:
            return user
        created = await self._database.upsert_user(telegram_id, settings.timezone)
        if not created:
            return None
        return await self._database.get_user_by_telegram_id(telegram_id)

    def _infer_frequency_type(self, text: str) -> str:
        lowered = text.lower()
        if "custom" in lowered or "personnalis" in lowered:
            return FREQUENCY_CUSTOM
        if "week" in lowered or "semaine" in lowered or self._extract_days(text):
            return FREQUENCY_WEEKLY
        return FREQUENCY_DAILY

    def _extract_days(self, text: str) -> List[int]:
        lowered = text.lower()
        days = []
        for token, day_value in DAY_MAP.items():
            if token in lowered:
                days.append(day_value)
        return sorted(set(days))

    def _extract_time(self, text: str) -> Optional[str]:
        match = re.search(r"\b(\d{1,2})(?:h|:)(\d{2})\b", text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            return f"{hour:02d}:{minute:02d}"

        match = re.search(r"\b(\d{1,2})\s?(?:am|pm)\b", text, re.IGNORECASE)
        if match:
            hour = int(match.group(1))
            if "pm" in match.group(0).lower() and hour < 12:
                hour += 12
            return f"{hour:02d}:00"

        return None

    def _build_schedules(
        self,
        frequency_type: str,
        day_of_week: List[int],
        time_of_day: str,
    ) -> List[Dict[str, Any]]:
        schedules: List[Dict[str, Any]] = []
        if frequency_type == FREQUENCY_DAILY:
            schedules.append({"day_of_week": None, "time_of_day": time_of_day})
            return schedules

        if day_of_week:
            for day in day_of_week:
                schedules.append({"day_of_week": day, "time_of_day": time_of_day})
            return schedules

        schedules.append({"day_of_week": None, "time_of_day": time_of_day})
        return schedules

    def _normalize_time(self, value: Any) -> str:
        if hasattr(value, "strftime"):
            return value.strftime("%H:%M")
        return str(value)


habit_service = HabitService()
