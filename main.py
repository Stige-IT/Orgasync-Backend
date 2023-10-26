from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware

from auth.route import auth_router
from core.security import JWTAuth
from users.routes import router, user_router

app = FastAPI(version="0.0.1", title="Orgasync Rest API")
app.include_router(router)
app.include_router(user_router)
app.include_router(auth_router)

# middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())


@app.get("/")
async def root():
    return {"message": "Service Running..."}


