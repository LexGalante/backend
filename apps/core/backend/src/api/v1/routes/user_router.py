from typing import List, Any

from fastapi import APIRouter, Depends

from api.v1.dependency_injection import get_user_service
from api.v1.schemas.user_schema import UserGetSchema
from services.user_service import UserService
from models.user import User

router = APIRouter()


@router.get("/paginate", response_model=List[UserGetSchema])
def index(
    service: UserService = Depends(get_user_service),
    page: int = 1,
    page_size: int = 10
) -> List[UserGetSchema]:
    users: List[User] = service.get_all(page, page_size)

    return [UserGetSchema(**user) for user in users]


@router.get("/", response_model=List[UserGetSchema])
def get(
    service: UserService = Depends(get_user_service),
    email: str = None
) -> UserGetSchema:
    user: User = service.get_by_email(email)

    return UserGetSchema(**user)

