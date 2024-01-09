from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class LogBookActivityResponse(BaseModel):
    id: str
    id_logbook: str
    id_logbook_employee: str
    description: str
    rating: int
    image: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
