from ..pubsub_providers.redis_pubsub_provider import RedisPubSubProvider


def publish_data(channel, data):
    publisher = RedisPubSubProvider()
    pub_data = {'data': data, 'channel': channel}
    publisher.publish(channel, pub_data)
