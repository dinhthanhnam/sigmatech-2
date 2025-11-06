from functools import wraps
from .session_context import get_session, clear_session

def transactional(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        session = get_session()
        try:
            result = fn(*args, **kwargs)
            session.commit()
            return result
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            clear_session()
    return wrapper
