from pydantic import BaseModel


class UserResponseSchema(BaseModel):
    email: str
    active: bool

    class Config:
        orm_mode = True

