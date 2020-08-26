from datetime import datetime, timedelta
from typing import Any, Union

from bcrypt import gensalt, hashpw, checkpw
from jose import jwt

from .config import API_MINUTES_EXPIRE_TOKEN, API_SECRET


def encode_token_jwt(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=API_MINUTES_EXPIRE_TOKEN)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, API_SECRET, algorithm="HS256")

    return encoded_jwt


def decode_token_jwt(token: str) -> dict:
    decode = jwt.decode(token, API_SECRET, algorithms="HS256")

    return decode


def encrypt(text: str) -> str:
    to_crypt = bytes(text, 'utf-8')
    password = hashpw(to_crypt, gensalt())

    return password.decode('utf-8')


def validate(original: str, comparer: str) -> bool:
    return checkpw(original.encode('utf-8'), comparer.encode('utf-8'))
