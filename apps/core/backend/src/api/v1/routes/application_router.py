from fastapi import APIRouter, Depends

from api.v1.dependency_injection import get_dbcontext, get_current_user
from resources.dbcontext import DbContext
from models.user import User


router = APIRouter()


@router.get("/")
def index(
    dbcontext: DbContext = Depends(get_dbcontext),
    current_user: User = Depends(get_current_user)
):
    pass
