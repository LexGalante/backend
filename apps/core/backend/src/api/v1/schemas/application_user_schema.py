from pydantic import BaseModel


class ApplicationUserRequestSchema(BaseModel):
    user_id: int
