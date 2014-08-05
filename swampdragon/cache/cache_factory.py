from django.conf import settings
from ..cache import redis_cache_store, memory_cache_store

cache_store = None


def get_cache_store():
    if hasattr(settings, 'DRAGON_CACHE'):
        pass

    return memory_cache_store
