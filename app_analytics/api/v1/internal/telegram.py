import logging

from fastapi import APIRouter, HTTPException, status

from app.api.v1.internal.schemas.bot_info import GetBotInfoResponse
from app.api.v1.internal.schemas.telegram import (
    InitIntegrationRequest,
    InitIntegrationResponse,
    UpdateIntegrationRequest,
    UpdateIntegrationResponse,
    IntegrationResponse, InitLeadsIntegrationRequest, InitLeadsIntegrationResponse, SendLeadRequest, SendLeadResponse,
    AuthLinkResponse, UpdateLeadRequest, UpdateLeadResponse,
)
from app.application.dto.lead_data import LeadDataDTO
from app.application.use_cases.telegram.auth_token import GetAuthTokenUseCase, RefreshAuthTokenUseCase
from app.application.use_cases.telegram.init_integration import InitIntegrationUseCase
from app.application.use_cases.telegram.init_leads import InitLeadsUseCase
from app.application.use_cases.telegram.send_lead import SendLeadUseCase
from app.application.use_cases.telegram.get_bot_info import GetBotInfoUseCase
from app.application.use_cases.telegram.update_integration import (
    UpdateIntegrationUseCase,
)
from app.application.use_cases.telegram.update_lead import UpdateLeadUseCase

api_router = APIRouter(prefix="/telegram", tags=["Telegram"])

logger = logging.getLogger(__name__)


@api_router.post("/init-integration")
async def init_integration(request: InitIntegrationRequest) -> InitIntegrationResponse:
    result = await InitIntegrationUseCase.execute(
        convert_id=request.convert_id, bot_token=request.bot_token, start_message_text=request.start_message_text
    )
    if not result.success:
        logger.exception(
            "Failed to initialize AmoCRM integration",
            extra={
                "error_message": result.message,
                "convert_id": request.convert_id,
                "request_data": request.dict(),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.message
        )

    return InitIntegrationResponse(
        success=True, message=result.message, integration_id=result.integration_id
    )


@api_router.patch("/{integration_id}")
async def update_integration(
    integration_id: int, request: UpdateIntegrationRequest
) -> UpdateIntegrationResponse:
    result = await UpdateIntegrationUseCase.execute(
        integration_id=integration_id, start_message_text=request.start_message_text
    )

    if not result.success:
        logger.exception(
            "Failed to send message to Telegram",
            extra={
                "error_message": result.message,
                "convert_id": integration_id,
                "request_data": request.dict(),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.message
        )

    if not result.integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found"
        )

    return UpdateIntegrationResponse(
        success=True,
        message=result.message,
        integration=IntegrationResponse(
            id=result.integration.id,
            start_message_text=result.integration.start_message_text,
            status=result.integration.status,
            convert_id=result.integration.convert_id,
        ),
    )


@api_router.post("/init-leads-integration")
async def init_leads_integration(request: InitLeadsIntegrationRequest) -> InitLeadsIntegrationResponse:
    result = await InitLeadsUseCase.execute(
        convert_id=request.convert_id, bot_leads_token=request.bot_token, telegram_id=request.telegram_id
    )

    if not result.success:
        logger.exception(
            "Failed to initialize AmoCRM integration",
            extra={
                "error_message": result.message,
                "convert_id": request.convert_id,
                "request_data": request.dict(),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.message
        )

    return InitLeadsIntegrationResponse(
        success=True, message=result.message, integration_id=result.integration_id
    )


@api_router.post("/{integration_id}/update-lead")
async def update_lead(integration_id: int, request: UpdateLeadRequest) -> UpdateLeadResponse:
    result = await UpdateLeadUseCase.execute(
        integration_id=integration_id,
        lead_data=LeadDataDTO(
            convert_domain=request.convert_domain,
            content=request.content,
            communication_channel=request.communication_channel,
            sending_integrations=request.sending_integrations,
            utm_params=request.utm_params,
        ),
        message_map=request.message_map
    )

    if not result.success:
        logger.exception(
            "Failed to send message to Telegram",
            extra={
                "error_message": result.message,
                "convert_id": integration_id,
                "request_data": request.dict(),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.message
        )

    return UpdateLeadResponse(
        success=True,
        message=result.message,
        integration_id=result.integration_id
    )


@api_router.post("/{integration_id}/send-lead")
async def send_lead(integration_id: int, request: SendLeadRequest) -> SendLeadResponse:
    result = await SendLeadUseCase.execute(
        integration_id=integration_id,
        lead_data=LeadDataDTO(
            convert_domain=request.convert_domain,
            content=request.content,
            communication_channel=request.communication_channel,
            sending_integrations=request.sending_integrations,
            utm_params=request.utm_params,
        )
    )

    if not result.success:
        logger.exception(
            "Failed to send message to Telegram",
            extra={
                "error_message": result.message,
                "convert_id": integration_id,
                "request_data": request.dict(),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.message
        )

    return SendLeadResponse(
        success=True,
        message=result.message,
        integration_id=result.integration_id,
        message_map=result.message_map
    )


@api_router.get("/{integration_id}/auth-link")
async def get_auth_link(integration_id: int) -> AuthLinkResponse:
    result = await GetAuthTokenUseCase.execute(integration_id=integration_id)

    if not result.success:
        logger.exception(
            "Failed to send message to Telegram",
            extra={
                "error_message": result.message,
                "convert_id": integration_id,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.message
        )

    return AuthLinkResponse(
        success=True,
        auth_link=result.auth_link
    )


@api_router.post("/{integration_id}/auth-link/refresh")
async def refresh_auth_link(integration_id: int) -> AuthLinkResponse:
    result = await RefreshAuthTokenUseCase.execute(integration_id=integration_id)

    if not result.success:
        logger.exception(
            "Failed to send message to Telegram",
            extra={
                "error_message": result.message,
                "convert_id": integration_id,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.message
        )

    return AuthLinkResponse(
        success=True,
        auth_link=result.auth_link
    )


@api_router.get("/{integration_id}/bot-info", response_model=GetBotInfoResponse)
async def get_bot_info(integration_id: int) -> GetBotInfoResponse:
    result = await GetBotInfoUseCase.execute(integration_id=integration_id)

    if not result.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)

    return GetBotInfoResponse(
        success=result.success,
        message=result.message,
        bot_token=result.bot_token,
        bot_leads_token=result.bot_leads_token,
        bot_name=result.bot_name,
        auth_link=result.auth_link,
        status=result.status
    )
