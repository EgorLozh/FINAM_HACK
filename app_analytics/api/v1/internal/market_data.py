import logging

from fastapi import APIRouter, Request, HTTPException, status

from app_analytics.api.v1.internal.schemas import PostMarketDataRequestSchema
from app_analytics.application.use_cases import PostMarketDataUseCase

api_router = APIRouter(prefix="/market_data")

logger = logging.getLogger(__name__)

@api_router.post("/")
async def post_market_data(request: Request, market_data_request: PostMarketDataRequestSchema) -> None:
    return await PostMarketDataUseCase.execute(market_data_request.data)




