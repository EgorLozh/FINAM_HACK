import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app_analytics.api.v1 import api_v1_router
from app_analytics.api.v1.middlewares.logging import RequestLoggerMiddleware
from app_analytics.core.config import settings
from app_analytics.core.http_client import close_global_httpx_client, init_global_httpx_client
from app_analytics.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    logger.info("Application startup: Calling init_global_httpx_client...")
    # Инициализируем HTTP клиент
    await init_global_httpx_client()

    logger.info(
        "Application startup complete (main lifespan).",
        extra={"LOG_LEVEL": settings.LOG_LEVEL},
    )

    yield  # Application runs here

    # Shutdown
    logger.info("Application shutdown: Calling close_global_httpx_client...")
    await close_global_httpx_client()

    logger.info("Application shutdown (main lifespan).")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Finam Hack Analytics Service",
        version="0.1.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_prefix="/api",
        lifespan=lifespan,
    )

    app.add_middleware(RequestLoggerMiddleware)

    app.include_router(api_v1_router)

    logger.info("FastAPI app created.")
    return app
