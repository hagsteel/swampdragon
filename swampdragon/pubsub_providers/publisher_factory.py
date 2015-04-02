from swampdragon.pubsub_providers import redis_publisher, mock_publisher
from swampdragon.testing import test_mode

_publisher = None


def get_publisher():
    global _publisher
    if not _publisher:
        if test_mode.test_mode():
            _publisher = mock_publisher.MockPublisher()
        else:
            _publisher = redis_publisher
    return _publisher
