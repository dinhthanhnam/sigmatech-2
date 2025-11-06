from contextvars import ContextVar
from sqlmodel import Session
from .db_context import engine, test_engine, set_test_engine, get_engine


_current_session: ContextVar[Session | None] = ContextVar("_current_session", default=None)

def get_session() -> Session:
    sess = _current_session.get()
    if sess is not None:
        return sess
    current_engine = get_engine()
    sess = Session(current_engine)
    _current_session.set(sess)
    return sess

def clear_session():
    _current_session.set(None)
