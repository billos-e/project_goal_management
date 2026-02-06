"""Domain models for Focus & Flow."""
from datetime import datetime, timezone as tz
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class User(BaseModel):
    """User domain model."""
    telegram_id: int = Field(..., description="Telegram user ID (primary key)")
    timezone: str = Field(default="Europe/Paris", description="User timezone for display")
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz.utc), description="UTC timestamp")


class HealthCheckResult(BaseModel):
    """Result of a component health check."""
    component: str
    status: str  # "ok" | "failed"
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(tz.utc))
