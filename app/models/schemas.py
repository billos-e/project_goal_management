"""API request and response schemas."""
from datetime import datetime, time, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Simple health check response."""
    status: str = Field(..., description="Health status: ok")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DetailedHealthResponse(BaseModel):
    """Detailed health check with component status."""
    status: str = Field(..., description="Overall health: healthy|degraded|unhealthy")
    components: Dict[str, Any] = Field(..., description="Component-level health details")


class HabitScheduleCreate(BaseModel):
    """Schedule payload for habit creation."""
    day_of_week: Optional[int] = Field(None, ge=0, le=6, description="0=Monday .. 6=Sunday")
    time_of_day: time


class HabitCreate(BaseModel):
    """Habit creation payload."""
    title: str
    frequency_type: str = Field(..., description="daily|weekly|custom")
    schedules: Optional[list[HabitScheduleCreate]] = None


class HabitListItem(BaseModel):
    """Habit list response item."""
    id: str
    title: str
    frequency_type: str


class ObjectiveCreate(BaseModel):
    """Objective creation payload."""
    title: str
    deadline: datetime


class ObjectiveListItem(BaseModel):
    """Objective list response item."""
    id: str
    title: str
    deadline: datetime
    status: str
