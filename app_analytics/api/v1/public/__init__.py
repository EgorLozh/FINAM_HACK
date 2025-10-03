from fastapi import APIRouter
from app_analytics.api.v1.public.generation import api_router as generation_api_router

api_public_router = APIRouter(prefix="/public")

api_public_router.include_router(generation_api_router, tags=["Generation"])
