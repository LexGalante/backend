from pydantic import BaseModel


class ApplicationEnvironmentRequestSchema(BaseModel):
    environment_id: int
