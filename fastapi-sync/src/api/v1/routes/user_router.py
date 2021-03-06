from typing import List, Optional

from api.v1.dependency_injection import get_dbcontext, get_current_user
from api.v1.schemas.user_schema import UserResponseSchema
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from resources.dbcontext import DbContext
from services.user_service import UserService

router = APIRouter()


@router.get("/paginate/{page}/{page_size}", response_model=List[UserResponseSchema])
def get(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user),
    page: Optional[int] = 1,
    page_size: Optional[int] = 10
) -> List[UserResponseSchema]:
    users: List[User] = UserService(dbcontext).get_all(page, page_size)

    return [UserResponseSchema.from_orm(user) for user in users]


@router.get("/{email}", response_model=UserResponseSchema)
def get_by_email(
    email: str,
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user),
) -> UserResponseSchema:
    user: User = UserService(dbcontext).get_by_email(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"{email} doesn't exists")

    return UserResponseSchema.from_orm(user)
