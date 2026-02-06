"""API route modules."""
from app.routes.health import router as health_router
from app.routes.telegram_webhook import router as telegram_router

__all__ = ["health_router", "telegram_router"]
