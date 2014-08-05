from django.conf import settings
from django.utils.importlib import import_module
from .redis_session_store import RedisSessionStore

session_store = None


def get_session_store():
    global session_store

    if session_store:
        return session_store
    try:
        module_name, cls_name = settings.DRAGON_SESSION_STORE.rsplit('.', 1)
        module = import_module(module_name)
        cls = getattr(module, cls_name)
        store = cls()
        session_store = store
    except:
        return RedisSessionStore()
