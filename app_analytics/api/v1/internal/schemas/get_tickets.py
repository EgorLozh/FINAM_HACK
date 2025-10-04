from pydantic import BaseModel, Field

class GetTicketsResponseSchema(BaseModel):
    tickets: list[str] = Field(..., description="List of ticket symbols")
