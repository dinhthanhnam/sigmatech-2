from sqlmodel import create_engine
from core.config import settings
from contextvars import ContextVar

engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True) #type: ignore

test_engine = create_engine(settings.test_database_url, echo=False, pool_pre_ping=True, isolation_level="AUTOCOMMIT") #type: ignore
