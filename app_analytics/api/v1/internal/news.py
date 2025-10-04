import logging

from fastapi import APIRouter, Request, HTTPException, status

from app_analytics.api.v1.internal.schemas.news import SaveNewRequestSchema, SaveNewResponseSchema
from app_analytics.application.use_cases.news.save_new import SaveNewUseCase

api_router = APIRouter(prefix="/news")

logger = logging.getLogger(__name__)


@api_router.post("/")
async def save_new(request: SaveNewRequestSchema) -> SaveNewResponseSchema:
    result = await SaveNewUseCase.execute(
        headline=request.headline,
        body=request.body,
        created_at=request.created_at,
        source=request.source,
        url=request.url
    )

    if not result.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)

    return SaveNewResponseSchema(
        headline=result.new.headline,
        body=result.new.body,
        created_at=result.new.created_at,
        source=result.new.source,
        url=result.new.url
    )
