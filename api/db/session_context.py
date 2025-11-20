from contextvars import ContextVar
from sqlmodel import Session
from .engines import engine


_current_session: ContextVar[Session | None] = ContextVar("_current_session", default=None)

def get_session() -> Session:
    sess = _current_session.get()
    if sess is not None:
        return sess
    sess = Session(engine)
    _current_session.set(sess)
    return sess

def set_session(sess):
    _current_session.set(sess)

def clear_session():
    _current_session.set(None)
