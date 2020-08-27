from starlette.responses import JSONResponse
from fastapi import Response, status


def ok() -> Response:
    return Response(status_code=status.HTTP_200_OK)


def created() -> Response:
    return Response(status_code=status.HTTP_201_CREATED)


def bad_request(body: str = None) -> Response:
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=body)


def unauthotized(body: str = None) -> Response:
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=body)
