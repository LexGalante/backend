from fastapi import APIRouter, Depends

from api.v1.dependency_injection import get_dbcontext
from resources.dbcontext import DbContext


router = APIRouter()


@router.post("/")
def index(db: DbContext = Depends(get_dbcontext)):
    pass
