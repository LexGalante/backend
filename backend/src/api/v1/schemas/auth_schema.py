from pydantic import BaseModel
from pydantic.networks import EmailStr


class AuthRequestSchema(BaseModel):
    username: EmailStr
    password: str

    class Config:
        orm_mode = True


class AuthResponseSchema(BaseModel):
    token_type: str
    access_token: str

    class Config:
        orm_mode = True
