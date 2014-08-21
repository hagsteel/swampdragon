from ..pubsub_providers.publisher_factory import get_publisher


def publish_data(channel, data):
    publisher = get_publisher()
    pub_data = {'data': data, 'channel': channel}
    publisher.publish(channel, pub_data)
