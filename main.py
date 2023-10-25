from fastapi import FastAPI

app = FastAPI(version="0.0.1", title="Orgasync Rest API")


@app.get("/")
async def root():
    return {"message": "Hello World"}


