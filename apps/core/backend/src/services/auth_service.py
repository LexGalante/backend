from models.user import User
from repositories.user_repository import UserRepository
from resources.dbcontext import DbContext
from resources.security import validate, encode_token_jwt


class AuthService():
    def __init__(self, dbcontext: DbContext):
        self._dbcontext: DbContext = dbcontext
        self._repository: UserRepository = UserRepository(dbcontext)

    def authenticate(self, email, password) -> str:
        user = self._repository.get_by_email(email)
        if user is None or not validate(password, user.password):
            raise ValueError("Invalid username or password")

        return self.generate_token(user)

    def generate_token(self, user: User):
        token: str = encode_token_jwt(user.email)

        return token
