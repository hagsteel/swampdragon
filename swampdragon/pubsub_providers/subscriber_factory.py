from .redis_sub_provider import RedisSubProvider
from .mock_sub_provider import MockSubProvider
import sys


_subscriber = None


def get_subscription_provider():
    global _subscriber
    if not _subscriber:
        if 'test' in sys.argv:
            _subscriber = MockSubProvider()
        else:
            _subscriber = RedisSubProvider()
    return _subscriber
