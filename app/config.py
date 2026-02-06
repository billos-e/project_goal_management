"""Application configuration management."""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Supabase
    supabase_url: str = "https://placeholder.supabase.co"  # Default for testing
    supabase_key: str = "placeholder-key"  # Default for testing
    supabase_service_role_key: Optional[str] = None

    # Telegram (skeleton - full values in Story 1.2)
    telegram_bot_token: Optional[str] = None
    telegram_webhook_secret: Optional[str] = None
    telegram_webhook_url: Optional[str] = None

    # Gemini (Story 1.3)
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-1.5-flash"

    # Application
    app_name: str = "focus-flow"
    environment: str = "production"
    log_level: str = "INFO"
    timezone: str = "Europe/Paris"


settings = Settings()
