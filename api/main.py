from fastapi import FastAPI
from fastapi.middleware import Middleware
from routes.crud.user import router as user_crud_router


app = FastAPI()
app.include_router(
    user_crud_router
    )


@app.get("/")
def hello():
    return { "message": "Hello world" }