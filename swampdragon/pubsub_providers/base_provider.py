from .channel_utils import make_safe


class PUBACTIONS:
    created = 'created'
    updated = 'updated'
    deleted = 'deleted'


class BaseProvider(object):
    def _construct_channel(self, base_channel, **channel_filter):
        sorted_filter_keys = sorted(channel_filter, key=channel_filter.get)
        filter_string = '|'.join(['{}:{}'.format(k, make_safe(channel_filter[k])) for k in sorted_filter_keys])
        complete_channel = '{}|{}'.format(base_channel, filter_string)
        return complete_channel

    def get_channel(self, base_channel, **channel_filter):
        return self._construct_channel(base_channel, **channel_filter)
