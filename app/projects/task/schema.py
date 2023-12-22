from datetime import datetime
from typing import Union
from pydantic import BaseModel


class TaskRequest(BaseModel):
    title: Union[str, None] = None
    description: Union[str, None] = None
    id_status: Union[str, None] = None
    id_priority: Union[str, None] = None
    id_employe_project: Union[str, None] = None
    start_date: Union[datetime, None] = None
    end_date: Union[datetime, None] = None
