import sys
from swampdragon.pubsub_providers import redis_publisher, mock_publisher

_publisher = None


def get_publisher():
    global _publisher
    if not _publisher:
        if 'test' in sys.argv:
            _publisher = mock_publisher.MockPublisher()
        else:
            _publisher = redis_publisher
    return _publisher
