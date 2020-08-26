import logging
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


logger = logging.getLogger(__name__)


async def http_error_handler(request: Request, error: HTTPException) -> JSONResponse:
    logger.error(error.detail)

    return JSONResponse({"errors": [error.detail]})
