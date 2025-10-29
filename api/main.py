from fastapi import FastAPI
from fastapi.middleware import Middleware
from routes import user_crud_router
from models.user import User


app = FastAPI()
app.include_router(
    user_crud_router
    )


@app.get("/")
def hello():
    return { "message": "Hello world" }

User.create({"username": "nam", "email": "nam@sigmatech.vn", "hashed_password": "123213"})