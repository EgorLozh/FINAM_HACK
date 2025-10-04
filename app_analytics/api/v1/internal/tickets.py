import logging

from fastapi import APIRouter, Request, HTTPException, status

from app_analytics.api.v1.internal.schemas import GetTicketsResponseSchema
from app_analytics.application.use_cases import GetTicketsUseCase

api_router = APIRouter(prefix="/tickets")

logger = logging.getLogger(__name__)

@api_router.get("/", response_model=GetTicketsResponseSchema)
async def get_tickets(request: Request) -> GetTicketsResponseSchema:
    """
    Эндпоинт для получения тикеров компаний.
    """
    return GetTicketsResponseSchema(tickets=GetTicketsUseCase.execute())