from fastapi import FastAPI
from fastapi.middleware import Middleware

app = FastAPI()

@app.get("/")
def hello():
  return { "message": "Hello world" };