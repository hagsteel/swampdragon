from datetime import date
from decimal import Decimal
from django.db.models.fields.files import ImageFieldFile, FileField
from ..serializers.serializer_importer import get_serializer
from ..models import get_property


class BaseSerializer(object):
    _serializers_set_ = False

    base_channel = None
    publish_fields = None
    update_fields = None
    type_name = None
    id_field = 'id'

    def __init__(self, context=None, **kwargs):
        self.context = context
        self.kwargs = kwargs
        self._set_field_serializers()

    def _set_field_serializers(self):
        if self._serializers_set_:
            return
        if not hasattr(self.__class__, '_serializers'):
            setattr(self.__class__, '_serializers', [])
        serializers = [s for s in dir(self) if s.endswith('_serializer')]
        for serializer in serializers:
            ser = getattr(self, serializer)
            if isinstance(ser, str):
                ser = get_serializer(ser, self.__class__)
                setattr(self, serializer, ser)

            if ser not in self.__class__._serializers:
                self.__class__._serializers.append(ser)
        self._serializers_set_ = True

    @classmethod
    def get_base_channel(cls):
        return cls.base_channel

    @classmethod
    def _get_type_name(cls):
        return cls.type_name

    @classmethod
    def get_publish_fields(cls):
        return cls.publish_fields

    def get_update_fields(self):
        return self.update_fields

    def get_publish_channel(self):
        return self.base_channel

    def serialize(self, obj, ignore_fields=[]):
        publish_fields = self.get_publish_fields()
        if not publish_fields:
            raise Exception('no publish fields set')
        data = dict({f: self._serialize_value(obj, f) for f in publish_fields if f not in ignore_fields})
        return data

    def compose_updated_data(self, instance, updated_data):
        data = dict(updated_data)
        data['_type'] = self._get_type_name()
        data[self.id_field] = getattr(instance, self.id_field)
        return data

    def _serialize_value(self, obj, attr_name):
        obj_serializer = getattr(self, '{}_serializer'.format(attr_name), None)
        if obj_serializer:
            obj_serializer = obj_serializer()
        if hasattr(self, 'serialize_{}'.format(attr_name)):
            m = getattr(self, 'serialize_{}'.format(attr_name))
            return m(obj, serializer=obj_serializer)

        val = get_property(obj, attr_name)

        if obj_serializer and hasattr(val, 'all'):
            return [obj_serializer.serialize(o) for o in val.all()]
        elif obj_serializer:
            return obj_serializer.serialize(val)

        if isinstance(val, date):
            return str(val)
        if isinstance(val, Decimal):
            return str(val)
        if isinstance(val, ImageFieldFile) or isinstance(val, FileField):
            try:
                return val.url
            except:
                return None
        return val
