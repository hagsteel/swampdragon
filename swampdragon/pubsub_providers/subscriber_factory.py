from .redis_pubsub_provider import RedisPubSubProvider
from .mock_pubsub_provider import MockPubSubProvider
import sys

_subscriber = None

def get_subscription_provider():
    global _subscriber
    if not _subscriber:
        if 'test' in sys.argv:
            _subscriber = MockPubSubProvider()
        else:
            _subscriber = RedisPubSubProvider()
    return _subscriber
