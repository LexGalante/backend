from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError

from api.v1.dependency_injection import get_current_user, get_dbcontext
from models.user import User
from resources.dbcontext import DbContext
from services.application_service import ApplicationService
from api.v1.schemas.application_schema import ApplicationResponseSchema, ApplicationRequestSchema


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ApplicationResponseSchema])
def get(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user)
):
    applications = ApplicationService(dbcontext).get_all_by_user(current_user)

    return [ApplicationResponseSchema.from_orm(application) for application in applications]


@router.get("/{name}", status_code=status.HTTP_200_OK, response_model=ApplicationResponseSchema)
def get_by_name(
    name: str,
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user)
):
    try:
        application = ApplicationService(dbcontext).get_by_name(name, current_user)

        return ApplicationResponseSchema.from_orm(application)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)
def post(
    schema: ApplicationRequestSchema,
    dbcontex: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user)
):
    try:
        application = ApplicationService(dbcontex).create(schema.__dict__, current_user)

        return {
            "id": application.id,
            "name": application.name,
            "active": application.active
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{name}", status_code=status.HTTP_202_ACCEPTED)
def put(
    name: str,
    schema: ApplicationRequestSchema,
    dbcontex: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user)
):
    try:
        application = ApplicationService(dbcontex).update(schema.__dict__, name, current_user)

        return ApplicationResponseSchema.from_orm(application)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{name}/activate", status_code=status.HTTP_200_OK)
def activate(
    name: str,
    dbcontex: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user)
):
    try:
        application = ApplicationService(dbcontex).activate(name, current_user)

        return {
            "id": application.id,
            "name": application.name,
            "active": application.active
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{name}/inactive", status_code=status.HTTP_200_OK)
def inactive(
    name: str,
    dbcontex: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user)
):
    try:
        application = ApplicationService(dbcontex).inactive(name, current_user)

        return {
            "id": application.id,
            "name": application.name,
            "active": application.active
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
