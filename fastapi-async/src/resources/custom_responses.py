from starlette.responses import JSONResponse
from fastapi import Response, status


def ok() -> Response:
    return Response(status_code=status.HTTP_200_OK)


def created() -> Response:
    return Response(status_code=status.HTTP_201_CREATED)


def no_content() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def bad_request(body: str = None) -> Response:
    if type(body) in [list, tuple, set, dict]:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=body)
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": body})


def unauthotized(body: str = None) -> Response:
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=body)
