from sqlmodel import create_engine
from core.config import settings
from contextvars import ContextVar

engine = create_engine(settings.database_url, echo=True) #type: ignore

test_engine = create_engine(settings.test_database_url, echo=True) #type: ignore

_current_engine: ContextVar = ContextVar("_current_engine", default=engine)

def get_engine():
    return _current_engine.get()

def set_test_engine():
    _current_engine.set(test_engine)
