from ..pubsub_providers.base_provider import BaseProvider
from .connection_pool import get_connection

_channels = []
_subscribers = {}


class MockProvider(BaseProvider):
    def __init__(self):
        self._connection = get_connection()
        self._channels = _channels
        self._subscribers = _subscribers

    def get_channel(self, base_channel, **channel_filter):
        return self._construct_channel(base_channel, **channel_filter)

    def _get_channels_starting_with(self, base_channel):
        channels = []
        for c in self._channels:
            if str(c).startswith(base_channel):
                channels.append(c)
        return channels

    def get_channels(self, base_channel):
        return self._get_channels_starting_with(base_channel)

    def publish(self, channel, data):
        for c in self._channels:
            if c == channel:
                self._connection.send(data)

    def subscribe(self, channels, broadcaster):
        if not isinstance(channels, list):
            channels = [channels, ]
        for c in channels:
            if c not in self._channels:
                self._channels.append(c)
            if c not in self._subscribers:
                self._subscribers[c] = [broadcaster, ]
            else:
                if broadcaster not in self._subscribers[c]:
                    self._subscribers[c].append(broadcaster)

    def unsubscribe(self, channels, broadcaster):
        for c in channels:
            self._channels.remove(c)
            if c in self._subscribers and self._subscribers[c] is not None:
                self._subscribers[c].remove(broadcaster)
