from ..pubsub_providers.base_provider import PUBACTIONS
from ..pubsub_providers.model_channel_builder import filter_channels_by_model, filter_channels_by_dict
from ..pubsub_providers.publisher_factory import get_publisher


publisher = get_publisher()


def publish_model(model_instance, serializer, action, changes=None):
    if action is PUBACTIONS.updated and not changes:
        return

    if hasattr(serializer, '_cache'):
        serializer.remove_from_cache()

    base_channel = serializer.get_base_channel()
    all_model_channels = publisher.get_channels(base_channel)
    channels = filter_channels_by_model(all_model_channels, model_instance)

    if channels:
        if changes:
            publish_data = {'data': serializer.get_object_map_data()}
            publish_data['data'].update(changes)
        else:
            publish_data = dict({'data': serializer.serialize()})
        publish_data['action'] = action

        for c in channels:
            publish_data['channel'] = c
            publisher.publish(c, publish_data)

    if changes:
        previous_relevant_channels = filter_channels_by_dict(all_model_channels, changes)
        remove_from_channels = list(set(previous_relevant_channels) - set(channels))
        if not remove_from_channels:
            return
        publish_data = dict({'data': {'id': model_instance.pk}})
        publish_data['action'] = PUBACTIONS.deleted
        for c in remove_from_channels:
            publish_data['channel'] = c
            publisher.publish(c, publish_data)
