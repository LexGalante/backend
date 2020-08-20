from fastapi import APIRouter

from .routes import register_router
from .routes import login_router
from .routes import user_router
from .routes import application_router
from .routes import application_user_router


prefix = "/v1"
router: APIRouter = APIRouter()
router.include_router(
    router=register_router.router,
    prefix="/register",
    tags=["/v1/register"]
)
router.include_router(
    router=login_router.router,
    prefix="/login",
    tags=["/v1/login"]
)
router.include_router(
    router=user_router.router,
    prefix="/users",
    tags=["/v1/users"]
)
router.include_router(
    router=application_router.router,
    prefix="/applications",
    tags=["/v1/applications"]
)
router.include_router(
    router=application_user_router.router,
    prefix="/applications/{name}/users",
    tags=["/v1/applications/{name}/users"]
)
