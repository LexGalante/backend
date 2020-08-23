from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from api.v1.dependency_injection import get_current_user, get_dbcontext
from api.v1.schemas.application_schema import ApplicationFeatureRequestSchema, ApplicationFeatureResponseSchema

from models.user import User
from models.application import Application
from resources.dbcontext import DbContext
from services.application_service import ApplicationService

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ApplicationFeatureResponseSchema])
def get(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user),
    name: str = None
):
    try:
        application = ApplicationService(dbcontext).get_by_name(name, current_user)
        features: List[ApplicationFeatureResponseSchema] = [ApplicationFeatureResponseSchema(
            environment_id=feature.environment_id,
            environment=feature.environment.name,
            name=feature.name,
            enable=feature.enable) for feature in application.features]

        return features
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=str(e))


@router.patch("/", status_code=status.HTTP_200_OK, response_model=List[ApplicationFeatureResponseSchema])
def patch(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user),
    schema: ApplicationFeatureRequestSchema = None,
    name: str = None,
):
    try:
        data = schema.__dict__
        service = ApplicationService(dbcontext)
        application: Application = None
        if "all" in data.keys() and data["all"]:
            application = service.add_feature_all_environments(name, data, current_user)
        else:
            application = service.add_feature(name, data, current_user)
        features: List[ApplicationFeatureResponseSchema] = [ApplicationFeatureResponseSchema(
            environment_id=feature.environment_id,
            environment=feature.environment.name,
            name=feature.name,
            enable=feature.enable) for feature in application.features]

        return features
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The feature({schema.name}) already exists this environment"
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=str(e))


@router.patch(
    "/{feature_name}/{environment_id}/activate",
    status_code=status.HTTP_200_OK,
    response_model=List[ApplicationFeatureResponseSchema]
)
def activate(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user),
    name: str = None,
    environment_id: int = None,
    feature_name: str = None
):
    try:
        application = ApplicationService(dbcontext).activate_feature(name, environment_id, feature_name, current_user)
        features: List[ApplicationFeatureResponseSchema] = [ApplicationFeatureResponseSchema(
            environment_id=feature.environment_id,
            environment=feature.environment.name,
            name=feature.name,
            enable=feature.enable) for feature in application.features]

        return features
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=str(e))


@router.patch("/activate-all", status_code=status.HTTP_200_OK, response_model=List[ApplicationFeatureResponseSchema])
def activate_all(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user),
    name: str = None
):
    try:
        application = ApplicationService(dbcontext).activate_all_feature(name, current_user)
        features: List[ApplicationFeatureResponseSchema] = [ApplicationFeatureResponseSchema(
            environment_id=feature.environment_id,
            environment=feature.environment.name,
            name=feature.name,
            enable=feature.enable) for feature in application.features]

        return features
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=str(e))


@router.patch(
    "/{feature_name}/{environment_id}/inactivate",
    status_code=status.HTTP_200_OK,
    response_model=List[ApplicationFeatureResponseSchema]
)
def inactivate(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user),
    name: str = None,
    environment_id: int = None,
    feature_name: str = None
):
    try:
        application = ApplicationService(dbcontext).inactivate_feature(name, environment_id, feature_name, current_user)
        features: List[ApplicationFeatureResponseSchema] = [ApplicationFeatureResponseSchema(
            environment_id=feature.environment_id,
            environment=feature.environment.name,
            name=feature.name,
            enable=feature.enable) for feature in application.features]

        return features
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=str(e))


@router.patch("/inactivate-all", status_code=status.HTTP_200_OK, response_model=List[ApplicationFeatureResponseSchema])
def inactivate_all(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user),
    name: str = None
):
    try:
        application = ApplicationService(dbcontext).inactivate_all_feature(name, current_user)
        features: List[ApplicationFeatureResponseSchema] = [ApplicationFeatureResponseSchema(
            environment_id=feature.environment_id,
            environment=feature.environment.name,
            name=feature.name,
            enable=feature.enable) for feature in application.features]

        return features
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=str(e))


@router.delete("/{feature_name}", status_code=status.HTTP_200_OK, response_model=List[ApplicationFeatureResponseSchema])
def delete(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user),
    feature_name: str = None,
    environment_id: Optional[int] = 0,
    name: str = None
):
    try:
        service = ApplicationService(dbcontext)
        application: Application = None
        if environment_id > 0:
            application = service.remove_feature(name, feature_name, environment_id, current_user)
        else:
            application = service.remove_feature_all_environments(name, feature_name, current_user)
        features: List[ApplicationFeatureResponseSchema] = [ApplicationFeatureResponseSchema(
            environment_id=feature.environment_id,
            environment=feature.environment.name,
            name=feature.name,
            enable=feature.enable) for feature in application.features]

        return features
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=str(e))
