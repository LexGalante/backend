from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import ExpiredSignatureError, JWSSignatureError

from models.user import User
from resources.security import decode_token_jwt
from resources.dbcontext import DbContext
from services.user_service import UserService


def get_dbcontext() -> Generator:
    """
    Session DbContext
    """
    try:
        dbcontext: DbContext = DbContext()

        yield dbcontext
    finally:
        dbcontext.finish()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")


async def get_current_user(token: str = Depends(oauth2_scheme), dbcontext: DbContext = Depends(get_dbcontext)) -> User:
    try:
        email = decode_token_jwt(token)
        user = UserService(dbcontext).get_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        if not user.active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"User ({email}) inactive")

        return user
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except JWSSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid token")
