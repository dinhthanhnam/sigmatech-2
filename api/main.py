from fastapi import FastAPI
from fastapi.middleware import Middleware
from routes import user_crud_router, product_crud_router
from models.user import User
import i18n
from i18n import t
import os

i18n.load_path.append(os.path.join(os.path.dirname(__file__), "lang"))
i18n.set('locale', 'vi')
i18n.set('fallback', 'en')


app = FastAPI()
app.include_router(user_crud_router)
app.include_router(product_crud_router)


@app.get("/")
def hello():
    return {"message": i18n.t("common.hello")}