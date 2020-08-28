from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from api.v1.dependency_injection import get_current_user, get_application_service
from api.v1.schemas.application_schema import ApplicationResponseSchema, ApplicationRequestSchema
from services.application_service import ApplicationService
from resources.custom_responses import ok, created, bad_request


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ApplicationResponseSchema])
async def get(
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    applications = await service.get_all_by_user(current_user)

    return [ApplicationResponseSchema(**application) for application in applications]


@router.get("/{name}", status_code=status.HTTP_200_OK, response_model=ApplicationResponseSchema)
async def get_by_name(
    name: str,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        application = await service.get_by_name(name, current_user)

        return ApplicationResponseSchema(**application)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post(
    schema: ApplicationRequestSchema,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        await service.create(schema.__dict__, current_user)

        return created()
    except ValueError as e:
        return bad_request(str(e))


@router.put("/{name}", status_code=status.HTTP_200_OK)
async def put(
    name: str,
    schema: ApplicationRequestSchema,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        await service.update(schema.__dict__, name, current_user)

        return ok()
    except ValueError as e:
        return bad_request(str(e))


@router.patch("/{name}/activate", status_code=status.HTTP_200_OK)
async def activate(
    name: str,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        await service.activate(name, current_user)

        return ok()
    except ValueError as e:
        return bad_request(str(e))


@router.patch("/{name}/inactivate", status_code=status.HTTP_200_OK)
async def inactivate(
    name: str,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        await service.inactivate(name, current_user)

        return ok()
    except ValueError as e:
        return bad_request(str(e))
