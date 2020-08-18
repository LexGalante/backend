from typing import List, Optional

from fastapi import APIRouter, Depends

from api.v1.dependency_injection import get_dbcontext
from api.v1.schemas.user_schema import UserResponseSchema
from resources.dbcontext import DbContext
from services.user_service import UserService
from models.user import User

router = APIRouter()


@router.get("/paginate/{page}/{page_size}", response_model=List[UserResponseSchema])
def index(
    dbcontext: DbContext = Depends(get_dbcontext),
    page: Optional[int] = 1,
    page_size: Optional[int] = 10
) -> List[UserResponseSchema]:
    users: List[User] = UserService(dbcontext).get_all(page, page_size)

    return [UserResponseSchema.from_orm(user) for user in users]


@router.get("/{email}", response_model=UserResponseSchema)
def get(
    dbcontext: DbContext = Depends(get_dbcontext),
    email: str = None
) -> UserResponseSchema:
    user: User = UserService(dbcontext).get_by_email(email)

    return UserResponseSchema.from_orm(user)

