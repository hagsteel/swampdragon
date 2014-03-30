from .connection_pool import get_connection


class TestSubscriberPublisherClient(object):
    def __init__(self):
        self._channels = []
        self._subscribers = {}
        self._published_data = {}
        self._connection = get_connection()

    def publish(self, channel, data):
        if channel not in self._published_data:
            self._published_data[channel] = []
        self._published_data[channel].append(data)
        self._connection.sent_data.append(data)

    def get_channels(self, base_channel, filters):
        return self._connection.pub_sub.get_channels(base_channel, filters)
