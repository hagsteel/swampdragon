from .redis_pubsub_provider import RedisPubSubProvider
from .mock_pubsub_provider import MockPubSubProvider
import sys


def get_pubsub_provider():
    if 'test' in sys.argv:
        return MockPubSubProvider()
    return RedisPubSubProvider()