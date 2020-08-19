from typing import Optional

from datetime import datetime

from pydantic import BaseModel


class ApplicationRequestSchema(BaseModel):
    real_name: str
    model: int
    description: str
    details: Optional[str]
    active: Optional[bool]


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
