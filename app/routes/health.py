"""Health check endpoints."""
from datetime import datetime, timezone
from fastapi import APIRouter, status
from app.models.schemas import HealthResponse, DetailedHealthResponse
from app.services import database_service
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check() -> HealthResponse:
    """
    Simple liveness probe.

    Returns:
        Basic health status
    """
    logger.info("Health check endpoint called")
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc)
    )


@router.get("/detailed", response_model=DetailedHealthResponse, status_code=status.HTTP_200_OK)
async def detailed_health_check() -> DetailedHealthResponse:
    """
    Detailed system diagnostics.

    Returns:
        Component-level health status
    """
    logger.info("Detailed health check endpoint called")

    # Check database connectivity
    db_healthy = await database_service.health_check()
    db_status = "ok" if db_healthy else "failed"

    # Determine overall status
    overall_status = "healthy" if db_healthy else "degraded"

    components = {
        "api": "ok",
        "database": db_status,
        "database_error": None if db_healthy else "Connection failed",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return DetailedHealthResponse(
        status=overall_status,
        components=components
    )
