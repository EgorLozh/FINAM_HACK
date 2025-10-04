from fastapi import APIRouter, Depends

from app_analytics.api.v1.middlewares.auth import verify_internal_token
from app_analytics.api.v1.internal.news import api_router as api_news_router

api_internal_router = APIRouter(prefix="/internal", dependencies=[Depends(verify_internal_token)])

api_internal_router.include_router(api_news_router)
