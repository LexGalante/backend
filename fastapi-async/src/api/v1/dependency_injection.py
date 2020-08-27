from typing import Generator

from databases import Database
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import ExpiredSignatureError, JWSSignatureError, JWTError

from resources.security import decode_token_jwt
from resources.database import database
from services.user_service import UserService


def get_dbcontext() -> Generator:
    yield database


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")


async def get_current_user(token: str = Depends(oauth2_scheme), database: Database = Depends(get_dbcontext)):
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
