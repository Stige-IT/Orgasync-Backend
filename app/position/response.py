from pydantic import BaseModel


class PositionResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True
