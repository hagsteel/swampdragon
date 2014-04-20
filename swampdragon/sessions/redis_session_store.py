from django.conf import settings
from .session_store import BaseSessionStore
import redis


class RedisSessionStore(BaseSessionStore):
    def __init__(self):
        self.client = redis.StrictRedis()

    def save(self, key, val):
        self.client.set(key, val)
        self.client.expire(key, getattr(settings, 'SESSION_EXPIRATION_TIME', 30) * 60)

    def get(self, key):
        self.client.expire(key, getattr(settings, 'SESSION_EXPIRATION_TIME', 30) * 60)
        return self.client.get(key)
