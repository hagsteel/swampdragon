from django.core.exceptions import ValidationError
from django.db.models import ManyToManyField
from django.db.models.loading import get_model
from .base_serializer import BaseSerializer
from .object_map import get_object_map
from swampdragon.serializers.field_deserializers import get_deserializer


class DjangoModelSerializer(BaseSerializer):
    model = None
    include_related = []
    instance = None

    def __init__(self, instance=None, context=None, **kwargs):
        super(DjangoModelSerializer, self).__init__(context, **kwargs)
        self.base_channel = '{}'.format(self._model().__name__)
        if instance:
            self.instance = instance

    @classmethod
    def _model(cls):
        if isinstance(cls.model, str):
            cls.model = get_model(*cls.model.split('.', 1))
        return cls.model

    @classmethod
    def get_base_channel(cls):
        if cls.base_channel:
            return '{}|'.format(cls.base_channel)
        return '{}|'.format(cls._get_type_name())

    @classmethod
    def _get_type_name(cls):
        return cls._model()._meta.model_name

    @classmethod
    def get_related_fields(cls):
        pub_fields = cls.get_publish_fields()
        return [f for f in pub_fields if hasattr(cls._model(), f)]

    @classmethod
    def _get_publish_m2m_fields(cls):
        related_fields = cls.get_related_fields()
        m2m_fields = []
        for f in related_fields:
            field = getattr(cls._model(), f)
            if hasattr(field, 'field'):
                field = field.field
            elif hasattr(field, 'related'):
                field = field.related.field
            if isinstance(field, ManyToManyField):
                m2m_fields.append(f)
        return m2m_fields

    def is_valid(self, obj):
        try:
            obj.full_clean()
            return None
        except ValidationError as e:
            return e.message_dict

    def serialize(self, obj=None, ignore_fields=[]):
        if obj is None:
            obj = self.instance
        if obj is None:
            return None

        data = super(DjangoModelSerializer, self).serialize(obj, ignore_fields=ignore_fields)

        for m2m in self._get_publish_m2m_fields():
            val = getattr(obj, m2m)
            data['{}_id'.format(val.target_field_name)] = [v['pk'] for v in val.all().values('pk')]

        data['id'] = getattr(obj, self.id_field)
        data['_type'] = self._get_type_name()
        return data

    def deserialize(self, obj=None, initials=dict(), **kwargs):
        if obj is None:
            model_instance = self._model()()
        else:
            model_instance = obj

        for key, val in initials.items():
            self.deserialize_field(model_instance, key, val)

        for key, val in kwargs.items():
            if key not in self.update_fields:
                continue
            self.deserialize_field(model_instance, key, val)
            # field = model_instance._meta.get_field(key)
            # field_type = field.__class__.__name__
            # deserializer = get_deserializer(field_type)
            # if deserializer:
            #     deserializer(model_instance, key, val)
            # else:
            #     setattr(model_instance, key, val)

        return model_instance

    def deserialize_field(self, model_instance, key, val):
        field = model_instance._meta.get_field(key)
        field_type = field.__class__.__name__
        deserializer = get_deserializer(field_type)
        if deserializer:
            deserializer(model_instance, key, val)
        else:
            setattr(model_instance, key, val)


    @classmethod
    def get_object_map(cls, include_serializers=None, ignore_serializers=None):
        return get_object_map(cls, include_serializers, ignore_serializers)
