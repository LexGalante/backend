from pydantic import BaseModel


class UserResponseSchema(BaseModel):
    id: int
    email: str
    active: bool

    class Config:
        orm_mode = True


class UserChangePasswordSchema(BaseModel):
    new_password: str
    confirm_password: str


