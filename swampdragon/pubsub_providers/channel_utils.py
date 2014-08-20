from ..model_tools import string_to_list, get_property
from .channel_filters import filter_options, in_compare, term_match_check


try:
    from urllib.parse import quote_plus, unquote_plus
except ImportError:
    from urllib import quote_plus, unquote_plus


def make_safe(val):
    """
    Make strings in filters save.
    i.e 'foo bar' becomes 'foo+bar'
    """
    if not isinstance(val, str):
        return val
    return quote_plus(val)


def remove_channel_filter(channel):
    """
    Remove filters from channel strings
    i.e foo_contains becomes foo
    """
    if '__' not in channel:
        return channel
    chan, channel_filter = channel.rsplit('__', 1)
    if filter_options.get(channel_filter):
        return chan
    return channel


def get_channel_filter(channel):
    if '__' not in channel:
        return filter_options['eq']
    chan, channel_filter_name = channel.rsplit('__', 1)
    channel_filter = filter_options.get(channel_filter_name)
    if not channel_filter:
        return filter_options['eq']
    return channel_filter


def get_property_and_value_from_channel(channel):
    """
    Get a list of tuples with properties and channels.
    i.e foo|bar__name__contains:baz returns a list: [('bar__name__contains', 'baz')]
    """
    filters = filter(None, str(channel).split('|')[1:])
    if not filters:
        return None
    properties = []
    for channel_filter, val in [tuple(f.split(':', 1)) for f in filters]:
        filter_option = filter_options.get(channel_filter.split('__')[-1])
        if filter_option == in_compare:
            val = string_to_list(val)
        properties.append((channel_filter, val))
    return properties


def channel_match_check(channel, data):
    terms = filter(None, channel.split('|')[1:])
    option = None
    for term in terms:
        key, val = term.split(':')
        if '__' in key and key.split('__')[-1] in filter_options.keys():
            option = key.rsplit('__', 1)[-1]
        if key not in data:
            return False
        if not term_match_check(data[key], val, option):
            return False
    return True


def properties_match_channel_by_object(obj, channel_properties):
    result = True
    for prop, val in channel_properties:
        if not has_val(obj, prop, val) and not has_related_value(obj, prop, val):
            return False
    return result


def properties_match_channel_by_dict(dict, channel_properties):
    result = True
    for prop, val in channel_properties:
        if prop not in dict:
            return False
        val_type = type(val)
        if not val_type(dict[prop]) == val:
            return False
    return result


def get_value(obj, prop):
    data = {}
    val = get_property(obj, prop)
    if val:
        data[prop] = val
    return data


def has_val(obj, prop, val):
    obj_val = get_property(obj, remove_channel_filter(prop))
    if not obj_val:
        return False
    channel_filter = get_channel_filter(prop)
    return channel_filter(val, obj_val)


def has_related_value(obj, field, channel_val):
    if '__' not in field:
        filter_by_val = channel_val
        property_name = field
    else:
        property_name, filter_by_val = field.split('__', 1)
    attr = getattr(obj, property_name)
    if hasattr(attr, 'all'):
        return getattr(obj, property_name).filter(**{filter_by_val: channel_val}).exists()
    else:
        filter_query = {'pk': obj.pk}
        filter_query[field] = channel_val
        return obj.__class__.objects.filter(**filter_query).exists()
