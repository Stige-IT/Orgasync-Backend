from pydantic import BaseModel


class StatusResponse(BaseModel):
    id: str
    name: str
    color: str
    level: int

    class Config:
        from_attributes = True
