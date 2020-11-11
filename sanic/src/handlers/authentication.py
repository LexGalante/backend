from sanic.request import Request
from sanic_jwt.exceptions import AuthenticationFailed
from src.models.user import User
from tortoise.exceptions import DBConnectionError, DoesNotExist


async def authenticate(request: Request, *args, **kwargs):
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    try:
        if not email or not password:
            raise AuthenticationFailed("Missing email or password")
        user = await User.filter(email=email, password=password).first()
        if user is None:
            raise AuthenticationFailed("User not found")

        return user.dict()
    except DBConnectionError:
        raise AuthenticationFailed("Unavailable database")
    except DoesNotExist:
        raise AuthenticationFailed("User not found")


async def retrieve_user(request: Request, payload: dict, *args, **kwargs):
    if payload:
        email = payload.get('email')
        user = await User.filter(email=email).first()

        return user
    return None
