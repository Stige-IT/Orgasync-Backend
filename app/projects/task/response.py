from datetime import datetime
from typing import Union
from pydantic import BaseModel


class TaskResponse(BaseModel):
    id: str
    name: str
    description: str
    id_employee: Union[str, None] = None
    id_status: str
    id_project: str
    created_at: Union[datetime, None] = None
    start_date: Union[datetime, None] = None
    end_date: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None
