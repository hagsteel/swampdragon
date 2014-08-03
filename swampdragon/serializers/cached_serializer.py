from ..cache.cache_factory import get_cache_store
from ..serializers.model_serializer import ModelSerializer


class CacheModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CacheModelSerializer, self).__init__(*args, **kwargs)
        self._cache = get_cache_store()

    def get_cache_key(self):
        return 'cache_{}{}'.format(self.get_base_channel(), self.instance.pk)

    def remove_from_cache(self):
        key = self.get_cache_key()
        self._cache.remove(key)

    def serialize(self, ignore_serializers=None):
        key = self.get_cache_key()
        if self.instance:
            if self._cache.has_data(key):
                return self._cache.get_data(key)
        data = super().serialize(ignore_serializers=ignore_serializers)
        if data:
            self._cache.store_data(data, key, 30)
        return data
