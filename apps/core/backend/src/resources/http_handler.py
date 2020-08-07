import logging

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_error_handler(request: Request, error: HTTPException) -> JSONResponse:
    logging.error(f"Error ocurred {error.detail}")
    return JSONResponse({"errors": [error.detail]})
