"""Global error handling middleware."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def catch_exceptions_middleware(request: Request, call_next):
    """
    Global exception handler middleware.

    Catches unhandled exceptions and returns structured error responses.
    """
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error(
            f"Unhandled exception: {str(exc)}",
            exc_info=True,
            extra={"path": request.url.path, "method": request.method}
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": "Internal server error",
                "timestamp": None
            }
        )
