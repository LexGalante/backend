from typing import List, Optional

from fastapi import APIRouter, Depends, status

from api.v1.dependency_injection import get_current_user, get_user_service
from api.v1.schemas.user_schema import (UserChangePasswordSchema,
                                        UserResponseSchema)
from resources.custom_responses import bad_request, no_content, ok
from services.user_service import UserService

router = APIRouter()


@router.get("/paginate/{page}/{page_size}", response_model=List[UserResponseSchema])
async def get(
    page: Optional[int] = 1,
    page_size: Optional[int] = 10,
    service: UserService = Depends(get_user_service),
    current_user: dict = Depends(get_current_user),
) -> List[UserResponseSchema]:
    users = await service.get_all(page, page_size)

    return [UserResponseSchema(**user) for user in users]


@router.get("/{email}", response_model=UserResponseSchema)
async def get_by_email(
    email: str,
    service: UserService = Depends(get_user_service),
    current_user: dict = Depends(get_current_user),
) -> UserResponseSchema:
    user = await service.get_by_email(email)
    if user is None:
        return no_content()

    return UserResponseSchema(**user)


@router.patch("/change-password", status_code=status.HTTP_200_OK)
async def patch(
    schema: UserChangePasswordSchema,
    service: UserService = Depends(get_user_service),
    current_user: dict = Depends(get_current_user),
):
    try:
        await service.change_password(current_user["email"], schema.new_password, schema.confirm_password)

        return ok()
    except ValueError as e:
        return bad_request(str(e))
