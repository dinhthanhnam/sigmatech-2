from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from fastapi.security import HTTPBearer, APIKeyHeader, OAuth2PasswordBearer
from routes import user_crud_router, product_crud_router, auth_router
from deps import auth_deps
from models import User
from core.i18n import setup_i18n
from i18n import t

setup_i18n()

app = FastAPI(dependencies=[*auth_deps])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [user_crud_router, product_crud_router, auth_router]
for router in routers:
    app.include_router(router)


@app.get("/")
def hello():
    return {"message": t("common.hello")}