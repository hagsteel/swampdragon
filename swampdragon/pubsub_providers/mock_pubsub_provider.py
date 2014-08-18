from ..pubsub_providers.base_provider import BaseProvider
from . import mock_publisher
from swampdragon.pubsub_providers.publisher_factory import get_publisher

_channels = []
publisher = get_publisher()


class MockPubSubProvider(BaseProvider):
    def __init__(self):
        self.publisher = publisher

    def publish(self, channel, data):
        connections = publisher.subscribers.get(channel, [])
        for c in connections:
            c.publish(data)

    def subscribe(self, channels, connection):
        connection.channels += channels
        for c in channels:
            if not c in publisher.subscribers.keys():
                publisher.subscribers[c] = []
            publisher.subscribers[c].append(connection)

    def unsubscribe(self, channels, connection):
        for c in channels:
            if c in connection.channels:
                connection.channels.remove(c)
            if c in publisher.subscribers.keys():
                if connection in publisher.subscribers[c]:
                    publisher.subscribers[c].remove(connection)
                if not publisher.subscribers[c]:
                    del publisher.subscribers[c]
        connection.channels = []

    def close(self, connection):
        self.unsubscribe(connection.channels, connection)
