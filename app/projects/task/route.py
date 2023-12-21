import uuid
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from app.projects.task.response import TaskResponse
from app.projects.task.schema import TaskRequest
from core.database import get_db
from core.security import oauth2_scheme
from app.projects.task.model import Task


task_router = APIRouter(
    prefix="/task",
    tags=["Task"],
    dependencies=[Depends(oauth2_scheme)],
)


# get all task
@task_router.get("", status_code=status.HTTP_200_OK, response_model=Page[TaskResponse])
async def get_task(id_project: str, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.id_project == id_project).all()
    return paginate(tasks)


# create new task
@task_router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    id_project: str, task_request: TaskRequest, db: Session = Depends(get_db)
):
    new_task = Task(
        id=uuid.uuid4(),
        name=task_request.title,
        description=task_request.description,
        id_status=task_request.id_status,
        id_project=id_project,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
