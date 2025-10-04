from pydantic import BaseModel

class PreprocessEventSchema(BaseModel):
    title: str
    country: str
    company: str
    ticket: str
    content: str