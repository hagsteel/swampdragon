try:
    from urllib.parse import quote_plus, unquote_plus
except ImportError:
    from urllib import quote_plus, unquote_plus


def make_safe(val):
    if not isinstance(val, str):
        return val
    return quote_plus(val)


def get_property_from_channel(channel):
    filter = channel.split('|')[1].split(':')[0]

    if filter.split('__')[-1] in filter_options.keys():
        prop = '__'.join(filter.split('__')[:-1])
    else:
        prop = '__'.join(filter.split('__'))
    return prop


def filter_matching_channels(channels, data):
    relevant_channels = []
    for channel in channels:
        if channel_match_check(channel, data):
            relevant_channels.append(channel)
    return relevant_channels


def channel_match_check(channel, data):
    terms = filter(None, channel.split('|')[1:])
    option = None
    for term in terms:
        key, val = term.split(':')
        if '__' in key and key.split('__')[-1] in filter_options.keys():
            key, option = key.rsplit('__', 1)
        if not key in data:
            return False
        if not term_match_check(data[key], val, option):
            return False
    return True


def term_match_check(term, val, option):
    decoded_val = unquote_plus(val)
    comparer = term_comparison_factory(option)
    return comparer(decoded_val, term)


def standard_compare(term, val):
    if val is None:
        return term is val
    term = type(val)(term)
    return term == (val)


def contains_compare(term, val):
    return term in val


def lt_compare(term, val):
    term = type(val)(term)
    return val < term


def lte_compare(term, val):
    term = type(val)(term)
    return val <= term


def gt_compare(term, val):
    term = type(val)(term)
    return val > term


def gte_compare(term, val):
    term = type(val)(term)
    return val >= term


filter_options = {
    'contains': contains_compare,
    'lt': lt_compare,
    'lte': lte_compare,
    'gt': gt_compare,
    'gte': gte_compare,
}


def term_comparison_factory(option):
    if option is None:
        return standard_compare
    return filter_options.get(option)
