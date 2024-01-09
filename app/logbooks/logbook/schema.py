from datetime import datetime
from typing import Union
from pydantic import BaseModel


class LogBookRequest(BaseModel):
    name: Union[str, None]
    description: Union[str, None]
    periode_start: datetime
    periode_end: datetime
