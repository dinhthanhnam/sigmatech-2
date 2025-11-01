from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, APIKeyHeader
from fastapi.middleware import Middleware
from routes import user_crud_router, product_crud_router
from models.user import User
import i18n
from i18n import t
import os

i18n.load_path.append(os.path.join(os.path.dirname(__file__), "lang"))
i18n.set('locale', 'vi')
i18n.set('fallback', 'en')
authorization_header = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

app = FastAPI(dependencies=[Depends(authorization_header), Depends(api_key_header)])
app.include_router(user_crud_router)
app.include_router(product_crud_router)


@app.get("/")
def hello():
    return {"message": i18n.t("common.hello")}