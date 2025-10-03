from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    success: bool
    message: str = ""


class ProcessWebhookResponse(BaseResponse):
    pass


class MessageGeneratedRequest(BaseModel):
    message_text: str = Field(..., description="Message text")
    chat_id: int = Field(..., description="Chat ID")
    message_id: int = Field(..., description="Message ID")
    convert_id: int = Field(..., description="Convert entity ID")


class MessageGeneratedResponse(BaseResponse):
    pass
