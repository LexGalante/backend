from datetime import datetime, timedelta
from typing import Any, Union

from bcrypt import gensalt, hashpw, checkpw
from jose import jwt

from .config import API_MINUTES_EXPIRE_TOKEN, API_SECRET


def genarate_jwt(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=API_MINUTES_EXPIRE_TOKEN
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, API_SECRET, algorithm="HS256")

    return encoded_jwt


def encrypt(text: str) -> str:
    return hashpw(text.encode('utf-8'), gensalt(12))


def validate(original: str, comparer: str) -> bool:
    return checkpw(original.encode('utf-8'), comparer.encode('utf-8'))
