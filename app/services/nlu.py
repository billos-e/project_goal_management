"""NLU service with Gemini integration and fallback templates."""
import json
import random
from typing import Any, Dict, Optional, Tuple

import httpx

from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class NLUService:
    """Service for intent detection with Gemini and fallback templates."""

    def __init__(self) -> None:
        """Initialize NLU service."""
        self._api_key = settings.gemini_api_key
        self._model = settings.gemini_model or "gemini-1.5-flash"

    def _fallback(self) -> Dict[str, str]:
        """
        Build a fallback response.

        Returns:
            Dict with intent and response_text
        """
        templates = [
            "Je n’ai pas tout compris, mais je vais faire comme si.",
            "Analyse incomplète. Réponse de secours activée.",
            "Mes circuits hésitent. Je réponds quand même.",
            "Intention floue. Mais votre détermination est notée.",
            "Fallback engagé. Je reste opérationnel, malgré tout.",
        ]
        return {
            "intent": "unknown",
            "response_text": random.choice(templates),
            "source": "fallback",
        }

    def _build_prompt(self, text: str) -> str:
        """
        Build the prompt for intent detection.

        Args:
            text: User input text

        Returns:
            Prompt string for Gemini
        """
        return (
            "Analyse the user message and return JSON only with keys: "
            "intent (string), response_text (string). "
            "Keep response_text in a TARS humorous/analytical tone. "
            f"User message: {text}"
        )

    async def identify_intent(self, text: str) -> Dict[str, str]:
        """
        Identify intent using Gemini with fallback on failure.

        Args:
            text: User input text

        Returns:
            Dict with intent, response_text, and source
        """
        if not self._api_key:
            logger.warning("GEMINI_API_KEY not configured, using fallback")
            return self._fallback()

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self._model}:generateContent"
        )
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": self._build_prompt(text)}
                    ]
                }
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.post(url, params={"key": self._api_key}, json=payload)
                response.raise_for_status()
                data = response.json()

            candidate_text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
            parsed = json.loads(candidate_text)

            return {
                "intent": str(parsed.get("intent", "unknown")),
                "response_text": str(parsed.get("response_text", "")),
                "source": "gemini",
            }
        except Exception as exc:
            logger.error(f"NLU failed, using fallback: {str(exc)}")
            return self._fallback()

    async def health_check(self) -> Tuple[bool, Optional[str]]:
        """
        Check Gemini connectivity.

        Returns:
            Tuple[bool, Optional[str]]: (ok, error_message)
        """
        if not self._api_key:
            return False, "GEMINI_API_KEY not configured"

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self._model}:generateContent"
        )
        payload = {
            "contents": [
                {"parts": [{"text": "ping"}]}
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.post(url, params={"key": self._api_key}, json=payload)
                response.raise_for_status()
            return True, None
        except Exception as exc:
            return False, str(exc)


nlu_service = NLUService()
