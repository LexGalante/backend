from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from resources.logger import Logger


async def http_error_handler(request: Request, error: HTTPException) -> JSONResponse:
    Logger.error(error.detail)

    return JSONResponse({"errors": [error.detail]})
