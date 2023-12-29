from datetime import datetime
from typing import Union
from pydantic import BaseModel
from app.projects.employee_company_project.response import (
    EmployeeCompanyProjectResponse,
)
from app.projects.priotity.response import PriorityResponse
from app.projects.status.response import StatusResponse


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    id_employee: Union[str, None] = None
    id_status: str
    id_project: str
    created_at: Union[datetime, None] = None
    start_date: Union[datetime, None] = None
    end_date: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None


class TaskItem(BaseModel):
    id: str
    id_project: str
    name: str
    description: Union[str, None] = None
    status: Union[StatusResponse, None] = None
    assignee: Union[EmployeeCompanyProjectResponse, None] = None
    priority: Union[PriorityResponse, None] = None
    start_date: datetime
    end_date: Union[datetime, None] = None
    created_at: datetime
    updated_at: Union[datetime, None] = None

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    done: list[TaskItem]
    todo: list[TaskItem]
    doing: list[TaskItem]

    class Config:
        from_attributes = True
