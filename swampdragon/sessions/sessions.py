from .redis_session_store import RedisSessionStore
from django.conf import settings
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module


session_store = None


def get_session_store():
    global session_store
    if session_store:
        return session_store

    if not hasattr(settings, 'SWAMP_DRAGON_SESSION_STORE'):
        session_store = RedisSessionStore
        return session_store
    else:
        try:
            module_name, cls_name = settings.SWAMP_DRAGON_SESSION_STORE.rsplit('.', 1)
            module = import_module(module_name)
            cls = getattr(module, cls_name)
            session_store = cls
        except:
            session_store = RedisSessionStore
        finally:
            return session_store
