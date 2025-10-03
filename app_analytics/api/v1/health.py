from fastapi import APIRouter, HTTPException, status

from app.application.use_cases.healthcheck.database_health import DatabaseHealthCheckUseCase

api_router = APIRouter(prefix="/health", tags=["Health"])


@api_router.get("", include_in_schema=True)  # Обрабатывает /health
@api_router.get("/", include_in_schema=True)  # Обрабатывает /health/
async def health_check() -> dict:
    result = await DatabaseHealthCheckUseCase.execute()
    if result.status:
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=result.message)
