from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.exc import IntegrityError

from api.v1.dependency_injection import get_dbcontext
from api.v1.schemas.register_schema import RegisterRequestSchema
from resources.dbcontext import DbContext
from services.user_service import UserService


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def index(dbcontext: DbContext = Depends(get_dbcontext), schema: RegisterRequestSchema = None):
    try:
        user = UserService(dbcontext).create(schema.__dict__)
        return {"id": user.id}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{schema.email} already exists!!!")
