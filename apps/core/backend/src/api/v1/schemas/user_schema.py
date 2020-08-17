from typing import List

from pydantic import BaseModel


class UserGetSchema(BaseModel):
    email: str
    active: bool

    class Config:
        orm_mode = True

