from contextvars import ContextVar
from sqlmodel import Session
from .db_context import engine


_current_session: ContextVar[Session | None] = ContextVar("_current_session", default=None)

def set_session(sess: Session):
    _current_session.set(sess)

def get_session() -> Session:
    sess = _current_session.get()
    if sess is not None:
        return sess
    sess = Session(engine)
    _current_session.set(sess)
    return sess

def clear_session():
    _current_session.set(None)
