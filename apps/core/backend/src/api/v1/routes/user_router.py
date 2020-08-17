from typing import List, Any, Optional

from fastapi import APIRouter, Depends

from api.v1.dependency_injection import get_dbcontext
from api.v1.schemas.user_schema import UserGetSchema
from resources.dbcontext import DbContext
from services.user_service import UserService
from models.user import User

router = APIRouter()


@router.get("/paginate/{page}/{page_size}", response_model=List[UserGetSchema])
def index(
    dbcontext: DbContext = Depends(get_dbcontext),
    page: Optional[int] = 1,
    page_size: Optional[int] = 10
) -> List[UserGetSchema]:
    users: List[User] = UserService(dbcontext).get_all(page, page_size)

    return [UserGetSchema.from_orm(user) for user in users]


@router.get("/{email}", response_model=UserGetSchema)
def get(
    dbcontext: DbContext = Depends(get_dbcontext),
    email: str = None
) -> UserGetSchema:
    user: User = UserService(dbcontext).get_by_email(email)

    return UserGetSchema.from_orm(user)

