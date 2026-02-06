"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import health_router, telegram_router
from app.middleware.error_handler import catch_exceptions_middleware
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info(
        f"Starting {settings.app_name} in {settings.environment} environment",
        extra={"timezone": settings.timezone}
    )
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


# Initialize FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Focus & Flow - AI-powered productivity assistant",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add middleware
app.middleware("http")(catch_exceptions_middleware)

# CORS configuration (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health_router)
app.include_router(telegram_router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Focus & Flow API",
        "version": "0.1.0",
        "docs": "/docs"
    }
