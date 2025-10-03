from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from app.core.config import settings

security = HTTPBearer()


async def verify_internal_token(request: Request) -> None:
    if request.url.path.startswith("/api/v1/internal"):
        try:
            authorization = request.headers.get("Authorization")
            if not authorization:
                raise HTTPException(status_code=403, detail="No authorization header")

            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme")

            if token != settings.INTERNAL_API_TOKEN:
                raise HTTPException(status_code=403, detail="Invalid token")
        except ValueError:
            raise HTTPException(status_code=403, detail="Invalid authorization header") from None
