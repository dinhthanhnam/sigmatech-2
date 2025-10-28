import pymysql
pymysql.install_as_MySQLdb()


from sqlmodel import create_engine, Session
from core.config import settings


engine = create_engine(settings.database_url, echo=True) #type: ignore


def get_session():
    with Session(engine) as session:
        yield session
