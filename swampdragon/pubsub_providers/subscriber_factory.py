from .redis_sub_provider import RedisSubProvider
from .mock_sub_provider import MockSubProvider
from swampdragon.testing import test_mode


_subscriber = None


def get_subscription_provider():
    global _subscriber
    if not _subscriber:
        if test_mode.test_mode():
            _subscriber = MockSubProvider()
        else:
            _subscriber = RedisSubProvider()
    return _subscriber
