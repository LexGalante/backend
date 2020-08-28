from typing import Generator

from databases import Database
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import ExpiredSignatureError, JWSSignatureError, JWTError

from resources.database import database
from resources.security import decode_token_jwt
from services.application_service import ApplicationService
from services.auth_service import AuthService
from services.environment_service import EnvironmentService
from services.user_service import UserService


def get_database() -> Generator:
    yield database


def get_user_service(database: Database = Depends(get_database)) -> Generator:
    user_service = UserService(database)

    yield user_service


def get_environment_service(database: Database = Depends(get_database)) -> Generator:
    environment_service = EnvironmentService(database)

    yield environment_service


def get_auth_service(
    database: Database = Depends(get_database),
    user_service: UserService = Depends(get_user_service)
) -> Generator:
    auth_service = AuthService(database, user_service)

    yield auth_service


def get_application_service(
    database: Database = Depends(get_database),
    user_service: UserService = Depends(get_user_service),
    environment_service: EnvironmentService = Depends(get_environment_service)
) -> Generator:
    service = ApplicationService(database, user_service, environment_service)

    yield service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")


async def get_current_user(token: str = Depends(oauth2_scheme), database: Database = Depends(get_database)):
    try:
        token = decode_token_jwt(token)
        email = token["sub"]
        user = await UserService(database).get_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        if not user["active"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"User ({email}) inactive")

        return user
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except JWSSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
