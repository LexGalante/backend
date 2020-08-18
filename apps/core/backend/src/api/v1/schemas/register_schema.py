import re

from pydantic import BaseModel, validator
from pydantic.networks import EmailStr


class RegisterRequestSchema(BaseModel):
    email: EmailStr
    password: str

    @validator("email")
    def email_validator(cls, value):
        if len(value) < 5 or len(value) > 250:
            raise ValueError("E-mail must contain between 5 and 250 characters")

        return value

    @validator("password")
    def password_validator(cls, value):
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', value):
            raise ValueError("""
                Password must contain the following rules: uppercase and lowercase letters, at least 8 characters
            """)

        return value

    class Config:
        orm_mode = True


