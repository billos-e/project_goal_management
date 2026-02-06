"""API request and response schemas."""
from datetime import datetime, timezone
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
