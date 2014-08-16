import redis
import json
import tornadoredis.pubsub
import tornadoredis
from .base_provider import BaseProvider


redis_client = redis.StrictRedis()
subscriber = tornadoredis.pubsub.SockJSSubscriber(tornadoredis.Client())


class RedisPubSubProvider(BaseProvider):
    def __init__(self):
        self._client = redis_client
        self._subscriber = subscriber

    def get_channels(self, base_channel):
        return self._get_channels_from_redis(base_channel)

    def close(self, broadcaster):
        for channel in broadcaster.channels:
            self._subscriber.unsubscribe(channel, broadcaster)

    def get_channel(self, base_channel, **channel_filter):
        return self._construct_channel(base_channel, **channel_filter)

    def subscribe(self, channels, broadcaster):
        broadcaster.channels += channels
        self._subscriber.subscribe(channels, broadcaster)

    def unsubscribe(self, channels, broadcaster):
        for channel in channels:
            self._subscriber.unsubscribe(channel, broadcaster)

    def _get_channels_from_redis(self, base_channel):
        channels = self._client.execute_command('PUBSUB', 'channels', '{}*'.format(base_channel))
        return [c.decode() for c in channels]

    def publish(self, channel, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        broadcasters = list(self._subscriber.subscribers[channel].keys())
        if broadcasters:
            for bc in broadcasters:
                if not bc.session.is_closed:
                    bc.broadcast(broadcasters, data)
                    break
