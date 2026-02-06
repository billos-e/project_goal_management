"""Objective service for creation and listing."""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

from app.config import settings
from app.services.database import database_service
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class ParsedObjective:
    title: str
    deadline_local: datetime


class ObjectiveService:
    """Service layer for objective operations."""

    def __init__(self) -> None:
        self._database = database_service

    async def create_objective(self, telegram_id: int, raw_text: str) -> Tuple[bool, str]:
        """
        Create an objective from a raw user command text.

        Args:
            telegram_id: Telegram user ID
            raw_text: Objective description from user

        Returns:
            Tuple[bool, str]: (success, response_text)
        """
        parsed = self._parse_objective(raw_text)
        if not parsed:
            return False, "Je ne comprends pas la deadline. Exemple: 'new goal: Finir le rapport demain 17h'."

        user = await self._get_or_create_user(telegram_id)
        if not user:
            return False, "Impossible d’identifier l’utilisateur. Diagnostic conseillé."

        deadline_utc = parsed.deadline_local.astimezone(ZoneInfo("UTC"))
        deadline_iso = deadline_utc.isoformat()

        created = await self._database.create_objective(
            user_id=str(user.get("id")),
            title=parsed.title,
            deadline_utc=deadline_iso,
        )
        if not created:
            return False, "Création échouée. Mes circuits refusent de coopérer."

        deadline_display = parsed.deadline_local.strftime("%d/%m/%Y %H:%M")
        response_text = (
            "Objectif enregistré. Chrono enclenché.\n"
            f"• {parsed.title}\n"
            f"• Deadline: {deadline_display} (Europe/Paris)"
        )
        return True, response_text

    async def list_objectives(self, telegram_id: int) -> List[Dict[str, Any]]:
        """
        List objectives for a telegram user.

        Args:
            telegram_id: Telegram user ID

        Returns:
            List of objective records
        """
        user = await self._database.get_user_by_telegram_id(telegram_id)
        if not user:
            return []
        return await self._database.list_objectives(str(user.get("id")))

    def format_objective_list(self, objectives: List[Dict[str, Any]]) -> str:
        """
        Format objective listing message.

        Args:
            objectives: List of objective records

        Returns:
            Formatted response text
        """
        if not objectives:
            return "Aucun objectif enregistré. Tu repousses l’échéance ?"

        lines = ["Vos objectifs :"]
        paris_tz = ZoneInfo(settings.timezone)
        for index, objective in enumerate(objectives, start=1):
            title = objective.get("title") or "(sans titre)"
            deadline = objective.get("deadline")
            deadline_text = "(deadline inconnue)"
            if deadline:
                parsed = self._parse_iso_datetime(deadline)
                if parsed:
                    deadline_text = parsed.astimezone(paris_tz).strftime("%d/%m/%Y %H:%M")
            lines.append(f"{index}. {title} — {deadline_text}")
        return "\n".join(lines)

    async def _get_or_create_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        user = await self._database.get_user_by_telegram_id(telegram_id)
        if user:
            return user
        created = await self._database.upsert_user(telegram_id, settings.timezone)
        if not created:
            return None
        return await self._database.get_user_by_telegram_id(telegram_id)

    def _parse_objective(self, raw_text: str) -> Optional[ParsedObjective]:
        text = raw_text.strip()
        if not text:
            return None

        title, deadline_text = self._split_title_deadline(text)
        if not title or not deadline_text:
            return None

        deadline_local = self._parse_deadline(deadline_text)
        if not deadline_local:
            return None

        return ParsedObjective(title=title, deadline_local=deadline_local)

    def _split_title_deadline(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        lowered = text.lower()
        for token in [" by ", " avant ", " pour "]:
            if token in lowered:
                idx = lowered.index(token)
                title = text[:idx].strip(" :")
                deadline = text[idx + len(token):].strip()
                return title, deadline
        return None, None

    def _parse_deadline(self, text: str) -> Optional[datetime]:
        lowered = text.lower()
        paris_tz = ZoneInfo(settings.timezone)
        now = datetime.now(paris_tz)

        if "tomorrow" in lowered or "demain" in lowered:
            base_date = (now + timedelta(days=1)).date()
        else:
            return None

        time_value = self._extract_time(lowered)
        if not time_value:
            return None

        hour, minute = time_value
        return datetime(
            base_date.year,
            base_date.month,
            base_date.day,
            hour,
            minute,
            tzinfo=paris_tz,
        )

    def _extract_time(self, text: str) -> Optional[Tuple[int, int]]:
        match = re.search(r"\b(\d{1,2})(?:h|:)(\d{2})\b", text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            return hour, minute

        match = re.search(r"\b(\d{1,2})\s?(am|pm)\b", text)
        if match:
            hour = int(match.group(1))
            minute = 0
            if match.group(2) == "pm" and hour < 12:
                hour += 12
            if match.group(2) == "am" and hour == 12:
                hour = 0
            return hour, minute

        return None

    def _parse_iso_datetime(self, value: Any) -> Optional[datetime]:
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(str(value))
        except (TypeError, ValueError):
            return None


objective_service = ObjectiveService()
