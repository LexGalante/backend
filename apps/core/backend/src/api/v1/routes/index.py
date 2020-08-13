from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def index() -> dict:
    return {"status": True, "message": "Ok!!!"}
