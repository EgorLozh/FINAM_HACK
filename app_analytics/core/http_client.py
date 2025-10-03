import logging

import httpx
from httpx_retries import Retry, RetryTransport

from app_analytics.core.config import settings

logger = logging.getLogger(__name__)


http_client: httpx.AsyncClient | None = None


async def init_global_httpx_client() -> None:
    global http_client

    if http_client is not None:
        logger.warning(
            "Global HTTPX client is already initialized. Skipping re-initialization.",
        )
        return

    logger.info("Initializing global HTTPX client with httpx-retries transport...")

    retry_strategy = Retry(
        total=settings.HTTPX_RETRY_TOTAL,
        backoff_factor=settings.HTTPX_RETRY_BACKOFF_FACTOR,
        max_backoff_wait=settings.HTTPX_RETRY_MAX_BACKOFF_WAIT,
        status_forcelist=settings.HTTPX_RETRY_STATUS_FORCELIST,
    )

    base_transport = httpx.AsyncHTTPTransport(
        verify=True,
    )

    custom_retry_transport = RetryTransport(
        retry=retry_strategy,
        transport=base_transport,
    )

    http_client = httpx.AsyncClient(
        timeout=settings.HTTPX_TIMEOUT,
        transport=custom_retry_transport,
    )
    logger.info(
        "Global HTTPX client with httpx-retries initialized successfully.",
        extra={
            "timeout_per_request": settings.HTTPX_TIMEOUT,
            "retry_total": settings.HTTPX_RETRY_TOTAL,
            "retry_backoff_factor": settings.HTTPX_RETRY_BACKOFF_FACTOR,
            "retry_max_backoff_wait": settings.HTTPX_RETRY_MAX_BACKOFF_WAIT,
            "retry_status_forcelist": settings.HTTPX_RETRY_STATUS_FORCELIST,
        },
    )


async def get_httpx_client() -> httpx.AsyncClient:
    if http_client is None:
        await init_global_httpx_client()

    if http_client is None:
        raise RuntimeError("Global HTTPX client was not initialized.")
    return http_client


async def close_global_httpx_client() -> None:
    global http_client
    if http_client:
        logger.info("Closing global HTTPX client...")
        await http_client.aclose()
        http_client = None
        logger.info("Global HTTPX client closed.")
    else:
        logger.info("Global HTTPX client was not initialized, no action to close.")
