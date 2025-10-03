import logging
import time
from uuid import uuid4

from fastapi import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class RequestLoggerMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope, receive)
        request_id = str(uuid4())
        start_time = time.time()

        logger = logging.getLogger("fastapi")

        # Логируем входящий запрос
        logger.info(
            "AmoCRM Service Incoming request",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method,
                "query_params": dict(request.query_params),
            },
        )

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                # Логируем завершение запроса при получении заголовков ответа
                response_time = time.time() - start_time
                logger.info(
                    "AmoCRM Service Request completed",
                    extra={
                        "request_id": request_id,
                        "path": request.url.path,
                        "method": request.method,
                        "status_code": message["status"],
                        "response_time": response_time,
                    },
                )
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            # Логируем ошибки
            logger.error(
                "AmoCRM Service Request failed",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "status_code": 500,
                },
            )
            raise
