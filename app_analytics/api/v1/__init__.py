from fastapi import APIRouter

from app_analytics.api.v1.public import api_public_router


api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(api_public_router)
