from pydantic import BaseModel


class PriorityResponse(BaseModel):
    id: str
    name: str
    level: int

    class Config:
        from_attributes = True
