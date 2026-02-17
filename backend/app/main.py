import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import detection, documents, health, humanization
from app.core.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title="Humanizer API",
        description="AI Text Detection & Humanization Platform",
        version="0.1.0",
    )

    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    application.include_router(health.router)
    application.include_router(detection.router)
    application.include_router(humanization.router)
    application.include_router(documents.router)

    @application.on_event("startup")
    async def startup_event():
        logger.info("Humanizer API starting up...")
        logger.info(f"CORS origins: {settings.cors_origins}")
        logger.info(f"Anthropic API configured: {bool(settings.anthropic_api_key)}")

    return application


app = create_app()
