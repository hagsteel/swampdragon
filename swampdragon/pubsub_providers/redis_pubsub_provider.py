import json
import redis
import tornadoredis.pubsub
import tornadoredis
from .base_provider import BaseProvider


class RedisPubSubProvider(BaseProvider):
    def __init__(self):
        self._client = redis.StrictRedis()
        self._async_client = tornadoredis.Client()
        self._subscriber = None

    def _get_subscriber(self):
        if not self._subscriber:
            self._subscriber = tornadoredis.pubsub.SockJSSubscriber(tornadoredis.Client())
        return self._subscriber

    def get_channels(self, base_channel):
        return self._get_channels_from_redis(base_channel)

    def close(self):
        if self._subscriber:
            self._subscriber.close()

    def get_channel(self, base_channel, **channel_filter):
        return self._construct_channel(base_channel, **channel_filter)

    def subscribe(self, channels, broadcaster):
        self._get_subscriber().subscribe(channels, broadcaster)

    def unsubscribe(self, channels, broadcaster):
        self._get_subscriber().unsubscribe(channels, broadcaster)

    def _get_channels_from_redis(self, base_channel):
        channels = self._client.execute_command('PUBSUB', 'channels', '{}*'.format(base_channel))
        return [c.decode() for c in channels]

    def publish(self, channel, data):
        self._client.publish(channel, json.dumps(data))
