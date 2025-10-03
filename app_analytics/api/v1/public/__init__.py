from fastapi import APIRouter
from app_analytics.api.v1.public.telegram import api_router as telegram_api_router

api_public_router = APIRouter(prefix="/public")

api_public_router.include_router(telegram_api_router, tags=["Telegram"])
