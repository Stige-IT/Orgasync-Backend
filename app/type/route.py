import uuid

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.type.model import TypeCompany
from core.database import get_db

type_company_router = APIRouter(
    prefix="/type",
    tags=["Type Company"],
)


@type_company_router.get("", status_code=status.HTTP_200_OK)
async def get_type_company(db: Session = Depends(get_db)):
    return db.query(TypeCompany).all()


@type_company_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_type_company_id(id: str, db: Session = Depends(get_db)):
    return db.query(TypeCompany).filter(TypeCompany.id == id).first()


@type_company_router.post("", status_code=status.HTTP_201_CREATED)
async def create_type_company(name: str, db: Session = Depends(get_db)):
    type_company = TypeCompany(
        id=uuid.uuid4(),
        name=name
    )
    db.add(type_company)
    db.commit()
    db.refresh(type_company)
    return JSONResponse(content={"message": "Create Successfully"}, status_code=status.HTTP_201_CREATED)


@type_company_router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_type_company(id: str, name: str, db: Session = Depends(get_db)):
    type_company_data = db.query(TypeCompany).filter(TypeCompany.id == id).first()
    type_company_data.name = name
    db.commit()
    return type_company_data


@type_company_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_type_company(id: str, db: Session = Depends(get_db)):
    type_company = db.query(TypeCompany).filter(TypeCompany.id == id).first()
    db.delete(type_company)
    db.commit()
    return {"message": "Delete Successfully"}
