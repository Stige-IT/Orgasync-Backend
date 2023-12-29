import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.projects.status.model import Status
from app.projects.task.response import TaskList, TaskResponse
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
@task_router.get("", status_code=status.HTTP_200_OK, response_model=TaskList)
async def get_task(id_project: str, db: Session = Depends(get_db)):
    result = {}
    status = db.query(Status).all()
    tasks = (
        db.query(Task)
        .join(Task.project)
        .filter(Task.id_project == id_project)
        .order_by(desc(Task.created_at))
        .all()
    )
    for stat in status:
        result[stat.name] = []
        for task in tasks:
            if stat.id == task.id_status:
                result[stat.name].append(task)

    # order by created at per status
    for key in result:
        result[key] = sorted(result[key], key=lambda k: k.created_at)
    return result


# create new task
@task_router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    id_project: str, task_request: TaskRequest, db: Session = Depends(get_db)
):
    new_task = Task(
        id=uuid.uuid4(),
        id_project=id_project,
        name=task_request.title,
        description=task_request.description,
        id_status=task_request.id_status,
        id_priority=task_request.id_priority,
        id_employee_project=task_request.id_employee_company_project,
        start_date=task_request.start_date,
        end_date=task_request.end_date,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {
        "message": "Task has been created.",
        "data": new_task,
    }


# update task
@task_router.put("/{id_task}", status_code=status.HTTP_200_OK)
async def update_task(
    id_task: str, task_request: TaskRequest, db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == id_task).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id_task} not found",
        )
    task.name = task_request.title
    task.description = task_request.description
    task.id_status = task_request.id_status
    task.id_priority = task_request.id_priority
    task.id_employee_project = task_request.id_employee_company_project
    task.start_date = task_request.start_date
    task.end_date = task_request.end_date
    db.commit()
    db.refresh(task)
    return task


# delete task
@task_router.delete("/{id_task}", status_code=status.HTTP_200_OK)
async def delete_task(id_task: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id_task).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id_task} not found",
        )
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}
