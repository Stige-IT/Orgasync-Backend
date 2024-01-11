import json
from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_pagination import Page, paginate
from sqlalchemy import desc, text
from sqlalchemy.orm import Session
from app.company.model import Company
from app.employee.model import Employee
from app.projects.company_project.model import CompanyProject
from app.projects.employee_company_project.model import EmployeeCompanyProject
from app.projects.employee_project.model import EmployeeProject
from app.projects.project.model import Project
from app.projects.status.model import Status
from app.projects.task.response import TaskItem, TaskList, TaskMe, TaskResponse
from app.projects.task.schema import TaskRequest
from app.users.model import UserModel
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


# get all task me
@task_router.get("/me", status_code=status.HTTP_200_OK, response_model=List[TaskMe])
async def get_task_me(request: Request, id_company: str, db: Session = Depends(get_db)):
    result = []
    tasks = []
    id_user = request.user.id
    employee = (
        db.query(EmployeeCompanyProject)
        .join(CompanyProject)
        .filter(CompanyProject.id_company == id_company)
        .join(Employee)
        .join(UserModel)
        .filter(UserModel.id == id_user)
        .all()
    )
    for emp in employee:
        task = (
            db.query(Task)
            .filter(Task.id_employee_project == emp.id)
            .join(Status)
            .filter(Status.level != 1)
            .all()
        )
        if task:
            for t in task:
                tasks.append(t)

    company_project = (
        db.query(CompanyProject).filter(CompanyProject.id_company == id_company).all()
    )
    for cp in company_project:
        project = db.query(Project).filter(Project.id_company_project == cp.id).all()
        for p in project:
            for task in tasks:
                if p.id == task.id_project:
                    result.append(
                        {
                            "id_company_project": cp.id,
                            "id_project": p.id,
                            "name_project": p.name,
                            "description_project": p.description,
                            "task": task,
                        }
                    )

    response = []
    for res in result:
        if response:
            for resp in response:
                if resp["id_project"] == res["id_project"]:
                    resp["task"].append(res["task"])
                    break
            else:
                data = {}
                data["id_company_project"] = res["id_company_project"]
                data["id_project"] = res["id_project"]
                data["name_project"] = res["name_project"]
                data["description_project"] = res["description_project"]
                data["task"] = []
                data["task"].append(res["task"])
                response.append(data)
        else:
            data = {}
            if res["id_project"] not in data:
                data["id_company_project"] = res["id_company_project"]
                data["id_project"] = res["id_project"]
                data["name_project"] = res["name_project"]
                data["description_project"] = res["description_project"]
                data["task"] = []
            data["task"].append(res["task"])
            response.append(data)
    return response


# get task by id
@task_router.get("/{id_task}", status_code=status.HTTP_200_OK, response_model=TaskItem)
async def get_task_by_id(id_task: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id_task).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id_task} not found",
        )
    return task


# create new task
@task_router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    request: Request,
    id_project: str,
    task_request: TaskRequest,
    db: Session = Depends(get_db),
):
    id_user = request.user.id
    employee = (
        db.query(EmployeeCompanyProject)
        .join(Employee)
        .join(UserModel)
        .filter(UserModel.id == id_user)
        .join(CompanyProject)
        .join(Project)
        .filter(Project.id == id_project)
        .first()
    )
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {request.user.name} not not registered in this project",
        )

    new_task = Task(
        id=uuid.uuid4(),
        id_project=id_project,
        title=task_request.title,
        description=task_request.description,
        id_status=task_request.id_status,
        id_priority=task_request.id_priority,
        id_employee_project=task_request.id_employee_company_project,
        start_date=task_request.start_date,
        end_date=task_request.end_date,
        created_by=employee.id,
        updated_by=employee.id,
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
    request: Request,
    id_task: str,
    task_request: TaskRequest,
    db: Session = Depends(get_db),
):
    id_user = request.user.id
    company_project = (
        db.query(CompanyProject)
        .join(Project)
        .join(Task)
        .filter(Task.id == id_task)
        .first()
    )
    employee = (
        db.query(EmployeeCompanyProject)
        .join(Employee)
        .join(UserModel)
        .join(CompanyProject)
        .filter(CompanyProject.id == company_project.id)
        .filter(UserModel.id == id_user)
        .first()
    )
    print(f"ID EMPLOYEE : {employee.id}")
    task = db.query(Task).filter(Task.id == id_task).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id_task} not found",
        )
    task.updated_by = employee.id
    task.title = task_request.title
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
