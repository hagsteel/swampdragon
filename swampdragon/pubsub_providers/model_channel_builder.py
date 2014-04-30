from django.db.models import OneToOneField, ManyToManyField
from django.db.models.related import RelatedObject
from .channel_utils import make_safe, get_property_and_value_from_channel, properties_match_channel_by_object, properties_match_channel_by_dict


def _construct_channel(base_channel, **channel_filter):
    sorted_filter_keys = sorted(channel_filter)
    filter_string = '|'.join(['{}:{}'.format(k, make_safe(channel_filter[k])) for k in sorted_filter_keys])
    complete_channel = '{}{}'.format(base_channel, filter_string)
    return complete_channel


def _prefix_channel_filter(var_name, **channel_filter):
    """
    Prefix the property with the related var name
    """
    cf = dict()
    for k, v in channel_filter.items():
        key = '{}__{}'.format(var_name, k)
        cf[key] = v
    return cf


def get_related_channels(serializer, related_serializers=None, **channel_filter):
    if related_serializers and serializer in related_serializers:
        related_serializers.remove(serializer)
    related_fields = [serializer._model()._meta.get_field_by_name(f)[0] for f in serializer.get_related_fields()]
    related_channels = []
    for field in related_fields:
        if isinstance(field, RelatedObject) or isinstance(field, OneToOneField) or isinstance(field, ManyToManyField):
            if hasattr(field, 'field'):
                field = field.field
                model = field.model
                var_name = field.name
            elif hasattr(field, 'related'):
                model = field.related.parent_model
                var_name = field.related.var_name
            else:
                continue
            if related_serializers:
                for rs in related_serializers:
                    if rs._model() == model:
                        channel = _construct_channel(rs.get_base_channel(), **_prefix_channel_filter(var_name, **channel_filter))
                        related_channels.append(channel)
                        related_channels += get_related_channels(rs, related_serializers, **_prefix_channel_filter(var_name, **channel_filter))
    return related_channels


def make_channels(serializer, related_serializers=None, property_filter=None):
    if related_serializers:
        copy_of_related_serializers = list(related_serializers)
    else:
        copy_of_related_serializers = None
    channels = []
    base_channel = serializer.get_base_channel()
    if property_filter:
        if isinstance(property_filter, list):
            for p in property_filter:
                channels.append(_construct_channel(base_channel, **p))
                channels += get_related_channels(serializer, copy_of_related_serializers, **p)
        else:
            channels.append(_construct_channel(base_channel, **property_filter))
            channels += get_related_channels(serializer, copy_of_related_serializers, **property_filter)
    else:
        channels.append(_construct_channel(base_channel))
        channels += get_related_channels(serializer, copy_of_related_serializers)
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
        if not '__' in field:
            filter_name = channel_val
            property_name = field
        else:
            property_name, filter_name = field.split('__', 1)
        attr = getattr(obj, property_name)
        if hasattr(attr, 'all'):
            if not getattr(obj, property_name).filter(**{filter_name: channel_val}).exists():
                return False
    return True
