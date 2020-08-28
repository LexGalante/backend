from databases import Database

from resources.security import validate, encode_token_jwt
from services.user_service import UserService


class AuthService:
    def __init__(self, database: Database, user_service: UserService):
        self._database: Database = database
        self._user_service: UserService = user_service

    async def authenticate(self, email, password) -> str:
        user = await self._user_service.get_by_email(email)
        if user is None or not validate(password, user["password"]):
            raise ValueError("Invalid username or password")

        return self.generate_token(user)

    def generate_token(self, user: dict):
        token: str = encode_token_jwt(user["email"])

        return token
