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

    def subscribe(self, channels, subscriber):
        for c in channels:
            if c not in subscribers.keys():
                subscribers[c] = []
            subscribers[c].append(subscriber)

    def unsubscribe(self, channels, subscriber):
        if not isinstance(channels, list):
            return self.unsubscribe([channels], subscriber)
        for channel in channels:
            subscribers[channel].remove(subscriber)

        empty_channels = [k for (k, v) in subscribers.items() if not v]
        for k in empty_channels:
            del subscribers[k]

    def remove_subscriber(self, subscriber):
        channels = [c for c in subscribers if subscriber in subscribers[c]]
        self.unsubscribe(channels, subscriber)
