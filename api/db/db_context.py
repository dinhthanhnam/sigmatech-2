from sqlmodel import create_engine
from core.config import settings


engine = create_engine(settings.database_url, echo=True) #type: ignore

test_engine = create_engine(settings.test_database_url, echo=True) #type: ignore