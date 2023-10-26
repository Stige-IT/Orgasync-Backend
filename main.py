from fastapi import FastAPI
from fastapi.responses import JSONResponse

from users.routes import router

app = FastAPI(version="0.0.1", title="Orgasync Rest API")
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Service Running..."}


