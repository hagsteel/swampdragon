from django.db.models import ForeignKey, OneToOneField
from django.db.models.loading import get_model
from swampdragon.model_tools import get_property
from swampdragon.serializers.field_serializers import serialize_field
from swampdragon.serializers.serializer_importer import get_serializer
from swampdragon.serializers.field_deserializers import get_deserializer


class ModelSerializerMeta(object):
    def __init__(self, options):
        self.publish_fields = getattr(options, 'publish_fields', ())
        self.update_fields = getattr(options, 'update_fields', ())
        self.model = getattr(options, 'model')
        if isinstance(self.model, str):
            self.model = get_model(*self.model.split('.', 1))


class ModelSerializer(object):
    def __init__(self, data=None, instance=None, initial=None):
        self.opts = ModelSerializerMeta(self.Meta)
        self.instance = instance or self.opts.model()
        self.data = data
        self.initial = initial or {}

    class Meta(object):
        pass

    def _get_base_fields(self):
        return [f.name for f in self.opts.model._meta.fields]

    def _get_related_fields(self):
        return [f for f in self.opts.update_fields if f not in self.base_fields]

    # def _get_fk_fields(self):

    def deserialize(self):
        # Set initial data
        for key, val in self.initial.items():
            setattr(self.instance, key, val)

        # Serialize base fields
        self.base_fields = self._get_base_fields()
        for key, val in self.data.items():
            if key not in self.opts.update_fields or key not in self.base_fields:
                continue
            self._deserialize_field(key, val)
        return self.instance

    def save(self):
        self.deserialize()
        self.instance.save()

        # Serialize related fields
        self.related_fields = self._get_related_fields()
        for key, val in self.data.items():
            if key not in self.related_fields:
                continue
            self._deserialize_related(key, val)
        return self.instance

    def _deserialize_field(self, key, val):
        if hasattr(self, key):
            serializer = self._get_related_serializer(key)
            value = serializer(val).save()
            setattr(self.instance, key, value)
            value.save()
            return

        field = self.opts.model._meta.get_field(key)
        field_type = field.__class__.__name__
        deserializer = get_deserializer(field_type)
        if deserializer:
            deserializer(self.instance, key, val)
        else:
            setattr(self.instance, key, val)

    def _deserialize_related(self, key, val):
        serializer = self._get_related_serializer(key)
        if isinstance(val, list):
            for v in val:
                related_instance = serializer(v).deserialize()
                getattr(self.instance, key).add(related_instance)

    def _get_related_serializer(self, key):
        serializer = getattr(self, key, None)
        if isinstance(serializer, str):
            return get_serializer(serializer, self.__class__)
        return serializer

    def serialize(self, ignore_serializers=None):
        data = {}
        for field in self.opts.publish_fields:
            data[field] = self._serialize_value(field, ignore_serializers)
        return data

    def _serialize_value(self, attr_name, ignore_serializers=None):
        obj_serializer = self._get_related_serializer(attr_name)

        # To prevent infinite recursion, allow serializers to be ignored
        if ignore_serializers and obj_serializer in ignore_serializers:
            return None

        # If there is a specific function
        if hasattr(self, 'serialize_{}'.format(attr_name)):
            serialize_function = getattr(self, 'serialize_{}'.format(attr_name))
            return serialize_function(self.instance, serializer=obj_serializer)

        val = get_property(self.instance, attr_name)

        # If we have one or more related models
        if obj_serializer and hasattr(val, 'all'):
            return [obj_serializer(instance=o).serialize(ignore_serializers=[self.__class__]) for o in val.all()]
        elif obj_serializer:
            return obj_serializer(instance=val).serialize(ignore_serializers=[self.__class__])

        # Serialize the field
        return serialize_field(val)
