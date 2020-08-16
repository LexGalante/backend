from typing import List, Any

from fastapi import APIRouter, Depends

from api.v1.dependency_injection import get_dbcontext
from api.v1.schemas.user_schema import UserGetSchema
from resources.dbcontext import DbContext
from services.user_service import UserService
from models.user import User

router = APIRouter()


@router.get("/paginate", response_model=List[UserGetSchema])
def index(
    dbcontext: DbContext = Depends(get_dbcontext),
    page: int = 1,
    page_size: int = 10
) -> List[UserGetSchema]:
    users: List[User] = UserService(dbcontext).get_all(page, page_size)

    return [UserGetSchema(**user) for user in users]


@router.get("/", response_model=List[UserGetSchema])
def get(
    dbcontext: DbContext = Depends(get_dbcontext),
    email: str = None
) -> UserGetSchema:
    user: User = UserService(dbcontext).get_by_email(email)

    return UserGetSchema(**user)

