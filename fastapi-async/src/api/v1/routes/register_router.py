from fastapi import APIRouter, Depends, status

from api.v1.dependency_injection import get_user_service
from api.v1.schemas.register_schema import RegisterRequestSchema
from resources.custom_responses import bad_request, created
from services.user_service import UserService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def index(
    schema: RegisterRequestSchema,
    service: UserService = Depends(get_user_service)
):
    try:
        await service.create(schema.__dict__)

        return created()
    except Exception as e:
        return bad_request(str(e))
