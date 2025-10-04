from pydantic import BaseModel

class PreprocessEventSchema(BaseModel):
    title: str
    companies: list[str]
    countries: list[str] 
    sectors: list[str]
    tickets: list[str]
    content: str

class InputArticleSchema(BaseModel):
    title: str
    content: str
