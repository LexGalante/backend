from fastapi import APIRouter

from .routes import user_router

prefix = "/v1"
router: APIRouter = APIRouter()
router.include_router(router=user_router.router, prefix="/users", tags=["users"])
