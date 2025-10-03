import logging

from fastapi import APIRouter, Request, HTTPException, status

from app_analytics.api.v1.public.schemas.generation import GenerationRequestSchema, GenerationResponseSchema

api_router = APIRouter(prefix="/generate")

logger = logging.getLogger(__name__)

@api_router.post("/", response_model=GenerationResponseSchema)
async def generate_text(request: GenerationRequestSchema) -> GenerationResponseSchema:
    pass # какая то логика по генерации или возвращению 