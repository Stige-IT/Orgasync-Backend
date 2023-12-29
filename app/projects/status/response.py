from pydantic import BaseModel


class StatusResponse(BaseModel):
    id: str
    name: str
    is_done: bool

    class Config:
        from_attributes = True
