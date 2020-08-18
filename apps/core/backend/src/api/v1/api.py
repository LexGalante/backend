from fastapi import APIRouter

from .routes import register_router
from .routes import token_router
from .routes import user_router


prefix = "/v1"
router: APIRouter = APIRouter()
router.include_router(router=register_router.router, prefix="/register", tags=["register"])
router.include_router(router=token_router.router, prefix="/token", tags=["token"])
router.include_router(router=user_router.router, prefix="/users", tags=["users"])
