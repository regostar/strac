from fastapi import APIRouter
from app.api.v1.endpoints import (
    file_apis,
)


api_router = APIRouter()
api_router.include_router(file_apis.router, prefix="/files", tags=["files"])
