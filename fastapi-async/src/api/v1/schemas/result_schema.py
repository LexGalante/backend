from pydantic import BaseModel


class ResultSchema(BaseModel):
    status: bool
    messages: str
    
