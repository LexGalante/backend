from typing import List

from fastapi import APIRouter, Depends, status

from api.v1.dependency_injection import get_current_user, get_application_service
from api.v1.schemas.application_schema import (
    ApplicationFeatureRequestSchema, ApplicationFeatureResponseSchema)
from services.application_service import ApplicationService
from resources.custom_responses import ok, bad_request

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ApplicationFeatureResponseSchema])
async def get(
    name: str,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        features = await service.get_application_features(name, current_user)

        return [ApplicationFeatureResponseSchema(**feature) for feature in features]
    except ValueError as e:
        return bad_request(str(e))


@router.patch("/", status_code=status.HTTP_200_OK)
async def patch(
    name: str,
    schema: ApplicationFeatureRequestSchema,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        await service.add_feature(name, schema.__dict__, current_user)
    except ValueError as e:
        return bad_request(str(e))
    else:
        return ok()


@router.patch("/{feature_name}/{environment}/activate", status_code=status.HTTP_200_OK)
async def activate(
    name: str,
    environment: str,
    feature_name: str,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        await service.activate_feature(name, environment, feature_name, current_user)
    except ValueError as e:
        return bad_request(str(e))
    else:
        return ok()


@router.patch("/activate-all", status_code=status.HTTP_200_OK)
async def activate_all(
    name: str,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        await service.activate_all_feature(name, current_user)
    except ValueError as e:
        return bad_request(str(e))
    else:
        return ok()


@router.patch("/{feature_name}/{environment}/inactivate", status_code=status.HTTP_200_OK)
async def inactivate(
    name: str,
    environment: str,
    feature_name: str,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        await service.inactivate_feature(name, environment, feature_name, current_user)
    except ValueError as e:
        return bad_request(str(e))
    else:
        return ok()


@router.patch("/inactivate-all", status_code=status.HTTP_200_OK)
async def inactivate_all(
    name: str,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        await service.inactivate_all_feature(name, current_user)
    except ValueError as e:
        return bad_request(str(e))
    else:
        return ok()


@router.delete("/{feature_name}", status_code=status.HTTP_200_OK)
async def delete(
    name: str,
    feature_name: str,
    current_user: dict = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    try:
        await service.remove_feature(name, feature_name, current_user)
    except ValueError as e:
        return bad_request(str(e))
    else:
        return ok()
