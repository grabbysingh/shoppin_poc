from fastapi import APIRouter

from app.api import autonomous

api_router = APIRouter()

api_router.include_router(autonomous.router, prefix="/autonomous", tags=["no human loop"])

