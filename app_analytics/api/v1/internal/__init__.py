from fastapi import APIRouter, Depends

from app.api.v1.middlewares.auth import verify_internal_token
from app.api.v1.internal.telegram import api_router as telegram_api_router

api_internal_router = APIRouter(prefix="/internal", dependencies=[Depends(verify_internal_token)])
api_internal_router.include_router(telegram_api_router)
