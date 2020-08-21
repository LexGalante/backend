from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator


class ApplicationRequestSchema(BaseModel):
    real_name: str
    model: int
    description: str
    details: Optional[str]

    @validator("real_name")
    def real_name_validator(cls, value):
        if len(value) < 3 or len(value) > 250:
            raise ValueError(
                "[real_name] field must contain between 3 and 250 characters")

        return value

    @validator("model")
    def model_validator(cls, value):
        if value not in (1, 2, 3):
            raise ValueError("[model] field must be between 1, 2, 3")

        return value

    @validator("description")
    def description_validator(cls, value):
        if len(value) < 10 or len(value) > 250:
            raise ValueError(
                "[description] field must contain between 25 and 250 characters")

        return value


class ApplicationResponseSchema(BaseModel):
    id: int
    name: str
    real_name: str
    model: int
    description: str
    details: str
    active: bool
    created_at: datetime
    created_by: int
    updated_at: datetime
    updated_by: int

    class Config:
        orm_mode = True


class ApplicationUserRequestSchema(BaseModel):
    user_id: int


class ApplicationFeatureRequestSchema(BaseModel):
    environment_id: int
    name: str
    enable: bool
    all: Optional[bool] = False

    @validator("name")
    def name_validator(cls, value):
        if len(value) < 3 or len(value) > 250:
            raise ValueError("[name] field must contain between 3 and 250 characters")

        return value


class ApplicationFeatureResponseSchema(BaseModel):
    environment_id: str
    environment: str
    name: str
    enable: bool

    class Config:
        orm_mode = True
