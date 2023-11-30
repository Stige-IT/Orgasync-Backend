from fastapi import FastAPI, HTTPException
from fastapi_pagination import add_pagination
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from app.projects.project.route import project_router
from app.position.routes import position_router
from app.address.route import address_router, address_auth_router
from app.auth.route import auth_router
from app.company.route import company_router, company_auth_router
from app.employee.route import employee_router
from app.projects.company_project.route import company_project_router
from app.projects.employee_project.route import employee_project_router
from app.type.route import type_company_router
from core.security import JWTAuth
from app.users.routes import router, user_router

app = FastAPI(
    version="0.0.1",
    title="Orgasync Rest API",
    description="Orgasync Rest API Documentation",
)
app.include_router(router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(company_router)
app.include_router(company_auth_router)
app.include_router(employee_router)
app.include_router(type_company_router)
app.include_router(position_router)
app.include_router(address_router)
app.include_router(address_auth_router)
app.include_router(company_project_router)
app.include_router(employee_project_router)
app.include_router(project_router)

# middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Service Running...",
        "documentation": "/docs",
    }


@app.get("/uploads/{path}")
async def get_file(path: str):
    try:
        return FileResponse(f"uploads/{path}")
    except Exception as e:
        return HTTPException(status_code=404, detail="File not found")


add_pagination(app)
