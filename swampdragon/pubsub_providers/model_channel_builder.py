from ..serializers.serializer_tools import get_serializer_relationship_field
from .channel_utils import make_safe, get_property_and_value_from_channel, properties_match_channel_by_object, properties_match_channel_by_dict


def _construct_channel(base_channel, **channel_filter):
    sorted_filter_keys = sorted(channel_filter)
    filter_string = '|'.join(['{}:{}'.format(k, make_safe(channel_filter[k])) for k in sorted_filter_keys])
    complete_channel = '{}{}'.format(base_channel, filter_string)
    return complete_channel


def _prefix_channel_filter(var_name, channel_filter):
    """
    Prefix the property with the related var name
    """
    return channel_filter.replace('|', '|{}__'.format(var_name))


def make_channels(serializer, related_serializers=None, property_filter=None, prefix=None):
    channels = []
    base_channel = serializer.get_base_channel()

    if property_filter:
        if not isinstance(property_filter, list):
            property_filter = [property_filter]
        for p in property_filter:
            channel_data = _construct_channel(base_channel, **p)
            if prefix:
                channel_data = _prefix_channel_filter(prefix, channel_data)
            channels.append(channel_data)
    else:
        channels.append(_construct_channel(base_channel))

    if related_serializers:
        for related_serializer in related_serializers:
            field_name = get_serializer_relationship_field(serializer, related_serializer)
            channels += make_channels(related_serializer, None, property_filter, field_name)
    return channels


def filter_channels_by_dict(channels, dict):
    result = []
    for channel in channels:
        channel_properties = get_property_and_value_from_channel(channel)
        if not channel_properties:
            result.append(channel)
            continue
        if properties_match_channel_by_dict(dict, channel_properties):
            result.append(channel)
    return result


def filter_channels_by_model(channels, obj):
    result = []
    for channel in channels:
        channel_properties = get_property_and_value_from_channel(channel)
        if not channel_properties:
            result.append(channel)
            continue
        if properties_match_channel_by_object(obj, channel_properties):
            result.append(channel)
    return result


def has_related_values(obj, properties):
    for field, channel_val in properties:
        if '__' not in field:
            filter_name = channel_val
            property_name = field
        else:
            property_name, filter_name = field.split('__', 1)
        attr = getattr(obj, property_name)
        if hasattr(attr, 'all'):
            if not getattr(obj, property_name).filter(**{filter_name: channel_val}).exists():
                return False
    return True
