import json


subscribers = {}


class MockPublisher(object):
    def __init__(self):
        self.subscribers = subscribers

    def publish(self, channel, message):
        subs = subscribers.get(channel)
        if not subs:
            return
        for subscriber in subs:
            if isinstance(message, str):
                message = json.dumps(message)
            subscriber.published_data.append(message)

    def _get_channels_from_subscriptions(self, base_channel):
        channels = [key for key in self.subscribers.keys() if key.startswith(base_channel)]
        return channels

    def get_channels(self, base_channel):
        return self._get_channels_from_subscriptions(base_channel)
