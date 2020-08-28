from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from api.v1.dependency_injection import (get_application_service,
                                         get_current_user)
from api.v1.schemas.application_schema import ApplicationUserRequestSchema
from resources.custom_responses import bad_request, ok
from services.application_service import ApplicationService

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[str])
async def get(
    name: str,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        users: List[str] = await service.get_application_users(name, current_user)

        return [user["email"] for user in users]
    except ValueError as e:
        return bad_request(str(e))


@router.patch("/{email}", status_code=status.HTTP_200_OK)
async def patch(
    name: str,
    email: str,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        await service.add_user(name, email, current_user)

        return ok()
    except ValueError as e:
        return bad_request(str(e))


@router.delete("/{email}", status_code=status.HTTP_200_OK)
async def delete(
    name: str,
    email: str,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        await service.remove_user(name, email, current_user)

        return ok()
    except ValueError as e:
        return bad_request(str(e))
