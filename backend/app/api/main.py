from fastapi import APIRouter
import logging
from app.api.routes import user_prompts
from app.config import settings


api_router = APIRouter()
api_router.include_router(user_prompts.router, tags=["prompts"])


# Private routes router (e.g., for debugging)
private_router = APIRouter(prefix="/debug", tags=["debug"])


@private_router.get("/health")
def health_check():
    return {"status": "ok"}


if settings.environment == "development":
    api_router.include_router(private_router)
