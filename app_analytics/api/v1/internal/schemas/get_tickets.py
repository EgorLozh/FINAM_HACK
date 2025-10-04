from pydantic import BaseModel, Field

class GetTicketsResponseSchema(BaseModel):
    tickets: list[tuple[str]] = Field(..., description="List of ticket symbols")
