import datetime

from pydantic import BaseModel, Field


class SaveNewRequestSchema(BaseModel):
    headline: str
    body: str
    created_at: datetime.datetime
    source: str
    url: str


class SaveNewResponseSchema(SaveNewRequestSchema):
    ...
