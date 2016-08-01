import json
import redis
from .redis_settings import get_redis_host, get_redis_port, get_redis_db, get_redis_password, get_redis_socket

_redis_cli = None


def get_redis_cli():
    global _redis_cli
    socket = get_redis_socket()
    if not _redis_cli and socket:
        _redis_cli = redis.StrictRedis(
            unix_socket_path=socket,
            port=get_redis_port(),
            db=get_redis_db(),
            password=get_redis_password()
        )
    elif not _redis_cli and not socket:
        _redis_cli = redis.StrictRedis(
            host=get_redis_host(),
            port=get_redis_port(),
            db=get_redis_db(),
            password=get_redis_password()
        )
    return _redis_cli


def publish(channel, message):
    get_redis_cli().publish(channel, json.dumps(message))


def _get_channels_from_redis(base_channel):
    channels = get_redis_cli().execute_command('PUBSUB', 'channels', '{}*'.format(base_channel))
    return [c.decode() for c in channels]


def get_channels(base_channel):
    return _get_channels_from_redis(base_channel)
