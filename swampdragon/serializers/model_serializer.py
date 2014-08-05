from django.core.exceptions import ValidationError
from swampdragon.model_tools import get_property, get_model
from swampdragon.serializers.field_serializers import serialize_field
from swampdragon.serializers.object_map import get_object_map
from swampdragon.serializers.serializer_importer import get_serializer
from swampdragon.serializers.field_deserializers import get_deserializer
from swampdragon.serializers.serializer_tools import get_serializer_relationship_field, get_id_mappings
from swampdragon.serializers.validation import ModelValidationError


class ModelSerializerMeta(object):
    def __init__(self, options):
        self.publish_fields = getattr(options, 'publish_fields', ())
        if isinstance(self.publish_fields, str):
            self.publish_fields = (self.publish_fields, )

        self.update_fields = getattr(options, 'update_fields', ())
        if isinstance(self.update_fields, str):
            self.update_fields = (self.update_fields, )

        self.model = get_model(getattr(options, 'model'))
        self.id_field = getattr(options, 'id_field', 'pk')
        self.base_channel = getattr(options, 'base_channel', self.model._meta.model_name)


class ModelSerializer(object):
    def __init__(self, data=None, instance=None, initial=None):
        if data and not isinstance(data, dict):
            raise Exception('data needs to be a dictionary')
        self.opts = ModelSerializerMeta(self.Meta)
        self._instance = instance
        self.data = data
        self.initial = initial or {}
        self.base_fields = self._get_base_fields()
        self.m2m_fields = self._get_m2m_fields()
        self.related_fields = self._get_related_fields()

    class Meta(object):
        pass

    @property
    def instance(self):
        # if not self._instance:
        #     self._instance = self.opts.model()
        return self._instance

    def _get_base_fields(self):
        return [f.name for f in self.opts.model._meta.fields]

    def _get_related_fields(self):
        return [f for f in self.opts.update_fields if f not in self.base_fields and f not in self.m2m_fields]

    def _get_m2m_fields(self):
        m2m_fields = [f.name for f in self.opts.model._meta.local_many_to_many]
        return [f for f in self.opts.update_fields if f in m2m_fields]

    def deserialize(self):
        # Set initial data
        if not self._instance:
            self._instance = self.opts.model()

        for key, val in self.initial.items():
            setattr(self.instance, key, val)

        # Serialize base fields
        for key, val in self.data.items():
            if key not in self.opts.update_fields or key not in self.base_fields:
                continue
            self._deserialize_field(key, val)
        return self.instance

    def save(self):
        self.deserialize()
        try:
            self.instance.clean_fields()
        except ValidationError as e:
            raise ModelValidationError(e.message_dict)
        self.instance.save()

        # Serialize related fields
        for key, val in self.data.items():
            if key not in self.related_fields:
                continue
            self._deserialize_related(key, val)

        # Serialize m2m fields
        for key, val in self.data.items():
            if key not in self.m2m_fields:
                continue
            self._deserialize_related(key, val, save_instance=True)
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

    def _deserialize_related(self, key, val, save_instance=False):
        serializer = self._get_related_serializer(key)
        if isinstance(val, list):
            for v in val:
                related_instance = serializer(v).deserialize()
                if save_instance:
                    related_instance.save()
                getattr(self.instance, key).add(related_instance)

    def _get_related_serializer(self, key):
        serializer = getattr(self, key, None)
        if isinstance(serializer, str):
            return get_serializer(serializer, self.__class__)
        return serializer

    def serialize(self, ignore_serializers=None):
        if not self.instance:
            return None
        data = {'id': getattr(self.instance, self.opts.id_field)}
        data['_type'] = self.opts.model._meta.model_name

        # Set all the ids for related models
        # so the datamapper can find the connection
        data.update(get_id_mappings(self))
        # Set the id value for related models, for the data mapper
        if ignore_serializers:
            for ser in ignore_serializers:
                via = '{}_id'.format(get_serializer_relationship_field(ser, self))
                if hasattr(self.instance, via):
                    data[via] = getattr(self.instance, via)

        # Serialize the fields
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

    @classmethod
    def get_object_map(cls, include_serializers=None, ignore_serializers=None):
        return get_object_map(cls, ignore_serializers)

    @classmethod
    def get_base_channel(cls):
        if hasattr(cls.Meta, 'base_channel'):
            return '{}|'.format(getattr(cls.Meta, 'base_channel'))
        return '{}|'.format(get_model(cls.Meta.model)._meta.model_name)

    @classmethod
    def get_related_serializers(cls):
        possible_serializers = [k for k in cls.__dict__.keys() if not k.startswith('_') and not k == 'Meta']
        serializers = []
        for possible_serializer in possible_serializers:
            val = getattr(cls, possible_serializer)
            if isinstance(val, str):
                val = get_serializer(val, cls)
            if hasattr(val, 'serialize'):
                serializers.append((val, possible_serializer))
        return serializers
