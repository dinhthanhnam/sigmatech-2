from functools import wraps
from .session_context import get_session, clear_session
from sqlalchemy import exc

def transactional(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        session = get_session()
        session._in_manual_transaction = True
        try:
            result = fn(*args, **kwargs)
            session.commit()
            return result
        except Exception:
            print("ROLLBACK!") 
            session.rollback()
            raise RuntimeError(f"Transactional failed: {exc.__class__.__name__}") from None
        finally:
            session._in_manual_transaction = False
            session.close()
            clear_session()
    return wrapper
