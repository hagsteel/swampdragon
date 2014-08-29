import json
import redis


def publish(channel, message):
    redis_cli = redis.StrictRedis()
    redis_cli.publish(channel, json.dumps(message))


def _get_channels_from_redis(base_channel):
    redis_cli = redis.StrictRedis()
    channels = redis_cli.execute_command('PUBSUB', 'channels', '{}*'.format(base_channel))
    return [c.decode() for c in channels]


def get_channels(base_channel):
    return _get_channels_from_redis(base_channel)
