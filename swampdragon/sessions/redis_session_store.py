from django.conf import settings
from ..pubsub_providers import redis_publisher
from .session_store import BaseSessionStore
import json


class RedisSessionStore(BaseSessionStore):
    def __init__(self, connection):
        super(RedisSessionStore, self).__init__(connection)
        self.client = redis_publisher.get_redis_cli()

    def get_complete_key(self, key):
        return 's:{}|k:{}'.format(self.connection.session.session_id, key)

    def set(self, key, val):
        if isinstance(val, dict):
            val = json.dumps(val)
        complete_key = self.get_complete_key(key)
        self.client.set(complete_key, val)
        self.client.expire(complete_key, getattr(settings, 'SESSION_EXPIRATION_TIME', 30) * 60)

    def get(self, key):
        complete_key = self.get_complete_key(key)
        val = self.client.get(complete_key)
        if not val:
            return None
        self.refresh_key_timeout(key)
        return val.decode()

    def refresh_key_timeout(self, key):
        complete_key = self.get_complete_key(key)
        self.client.expire(complete_key, getattr(settings, 'SESSION_EXPIRATION_TIME', 30) * 60)
