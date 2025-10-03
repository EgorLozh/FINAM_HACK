import logging

from fastapi import APIRouter, Request, HTTPException, status

from app.api.v1.public.schemas.telegram import ProcessWebhookResponse, MessageGeneratedRequest, MessageGeneratedResponse
from app.application.use_cases.telegram.process_generated_message import MessageGeneratedUseCase
from app.application.use_cases.telegram.process_webhook import ProcessWebhookUseCase

api_router = APIRouter(prefix="/telegram", tags=["Telegram"])

logger = logging.getLogger(__name__)


@api_router.post("/webhook/{webhook_token}")
async def webhook(request: Request, webhook_token: str) -> ProcessWebhookResponse:
    request_body = await request.body()

    result = await ProcessWebhookUseCase.execute(request_body=request_body, webhook_token=webhook_token)
    if not result.success:
        logger.exception(
            "Failed to process webhook",
            extra={
                "error_message": result.message,
            },
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)

    return ProcessWebhookResponse(success=True, message=result.message)


@api_router.post("/message-generated")
async def message_generated(request: MessageGeneratedRequest) -> MessageGeneratedResponse:
    result = await MessageGeneratedUseCase.execute(
        message_text=request.message_text,
        chat_id=request.chat_id,
        message_id=request.message_id,
        convert_id=request.convert_id
    )

    if not result.success:
        logger.exception(
            "Failed to send message to Telegram",
            extra={
                "error_message": result.message,
                "convert_id": request.convert_id,
                "request_data": request.dict(),
            },
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)

    return MessageGeneratedResponse(success=True, message=result.message)
