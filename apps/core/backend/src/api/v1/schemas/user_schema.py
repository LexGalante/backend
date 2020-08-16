from pydantic import BaseModel


class UserGetSchema(BaseModel):
    email: str
    active: bool
