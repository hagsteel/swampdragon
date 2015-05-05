from ..pubsub_providers.base_provider import PUBACTIONS
from ..pubsub_providers.model_channel_builder import filter_channels_by_model
from ..pubsub_providers.publisher_factory import get_publisher


publisher = get_publisher()


def publish_model(model_instance, serializer, action, changed_fields=None):
    if action is PUBACTIONS.updated and not changed_fields:
        return

    base_channel = serializer.get_base_channel()
    all_model_channels = publisher.get_channels(base_channel)
    channels = filter_channels_by_model(all_model_channels, model_instance)
    remove_from_channels = set(all_model_channels) - set(channels)

    if channels:
        publish_data = dict({'data': serializer.serialize(fields=changed_fields)})
        publish_data['action'] = action

        for c in channels:
            publish_data['channel'] = c
            publisher.publish(c, publish_data)

    if changed_fields:
        publish_data = {'data': {'id': model_instance.pk}}
        publish_data['action'] = PUBACTIONS.deleted
        for channel in remove_from_channels:
            publish_data['channel'] = channel
            publisher.publish(channel, publish_data)
            publish_data['channel'] = channel
