from databases import Database
from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError

from api.v1.dependency_injection import get_dbcontext
from api.v1.schemas.register_schema import RegisterRequestSchema
from services.user_service import UserService
from resources.custom_responses import created, bad_request

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def index(
    schema: RegisterRequestSchema,
    database: Database = Depends(get_dbcontext)
):
    try:
        service = UserService(database)
        await service.create(schema.__dict__)

        return created()
    except IntegrityError:
        return bad_request(f"{schema.email} already exists!!!")
