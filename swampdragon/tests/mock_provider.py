from ..pubsub_providers.base_provider import BaseProvider

_channels = []
_subscribers = {}


class MockPubSubProvider(BaseProvider):
    def __init__(self):
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
        connections = self._subscribers.get(channel, [])
        for c in connections:
            c.publish(data)

    def subscribe(self, channels, connection):
        if not isinstance(channels, list):
            channels = [channels, ]
        for c in channels:
            if c not in self._channels:
                self._channels.append(c)
            if c not in self._subscribers.keys():
                self._subscribers[c] = []
            if connection not in self._subscribers[c]:
                self._subscribers[c].append(connection)

    def unsubscribe(self, channels, connection):
        for c in channels:
            if c in self._subscribers and self._subscribers[c] is not None:
                self._subscribers[c].remove(connection)
                if not self._subscribers[c]:
                    self._subscribers.pop(c)
