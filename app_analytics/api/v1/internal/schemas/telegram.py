from typing import Optional

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    success: bool
    message: str = ""


class InitIntegrationRequest(BaseModel):
    convert_id: int = Field(..., description="Convert entity ID")
    bot_token: str = Field(..., description="Telegram bot token")
    start_message_text: str


class InitLeadsIntegrationRequest(BaseModel):
    convert_id: int = Field(..., description="Convert entity ID")
    bot_token: str = Field(..., description="Telegram bot token")
    telegram_id: int


class InitIntegrationResponse(BaseResponse):
    integration_id: Optional[int] = None


class InitLeadsIntegrationResponse(InitIntegrationResponse):
    ...


class UpdateIntegrationRequest(BaseModel):
    start_message_text: str = Field(..., description="Start message text")


class IntegrationResponse(BaseModel):
    id: int
    start_message_text: str
    status: str
    convert_id: int


class UpdateIntegrationResponse(BaseResponse):
    integration: IntegrationResponse


class SendLeadRequest(BaseModel):
    convert_domain: str
    content: dict
    communication_channel: str
    sending_integrations: list[str]
    utm_params: str


class UpdateLeadRequest(BaseModel):
    convert_domain: str
    content: dict
    communication_channel: str
    sending_integrations: list[str]
    utm_params: str
    message_map: dict[int, int]


class UpdateLeadResponse(BaseResponse):
    integration_id: Optional[int] = None


class SendLeadResponse(BaseResponse):
    integration_id: Optional[int] = None
    message_map: dict[int, int]


class AuthLinkResponse(BaseResponse):
    auth_link: str
