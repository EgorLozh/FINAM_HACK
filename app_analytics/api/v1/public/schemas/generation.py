from pydantic import BaseModel, Field


class GenerationResponseSchema(BaseModel):
    text: str = Field(description="The generated text.")


class GenerationRequestSchema(BaseModel):
    date_from: str = Field(description="The start date for the data range in YYYY-MM-DD format.")
    date_to: str = Field(description="The end date for the data range in YYYY-MM-DD format.")
