from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from api.v1.dependency_injection import get_current_user, get_dbcontext
from api.v1.schemas.application_schema import ApplicationUserRequestSchema
from models.user import User
from resources.dbcontext import DbContext
from services.application_service import ApplicationService

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[str])
def get(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user),
    name: str = None
):
    try:
        application = ApplicationService(dbcontext).get_by_name(name, current_user)
        users: List[str] = [str(user.user.email) for user in application.users]

        return users
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=str(e))


@router.patch("/", status_code=status.HTTP_200_OK)
def patch(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user),
    schema: ApplicationUserRequestSchema = None,
    name: str = None
):
    try:
        application = ApplicationService(dbcontext).add_user(
            name, schema.user_id, current_user)
        users: List[str] = [str(user.user.email) for user in application.users]

        return users
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The user({schema.user_id}) already exists this application"
        )


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user),
    user_id: int = None,
    name: str = None
):
    try:
        application = ApplicationService(
            dbcontext).remove_user(name, user_id, current_user)
        users: List[str] = [str(user.user.email) for user in application.users]

        return users
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
