from pydantic import BaseModel, Field


class GetBotInfoRequest(BaseModel):
    integration_id: int = Field(..., description="Integration ID")


class GetBotInfoResponse(BaseModel):
    success: bool
    message: str
    bot_token: str | None = None
    bot_leads_token: str | None = None
    bot_name: str | None = None
    auth_link: str | None = None
    status: str | None = None
