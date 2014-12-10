class SerializerMeta(object):
    def __init__(self, options):
        self.publish_fields = getattr(options, 'publish_fields', None)

        if isinstance(self.publish_fields, str):
            self.publish_fields = (self.publish_fields, )

        self.update_fields = getattr(options, 'update_fields', ())
        if isinstance(self.update_fields, str):
            self.update_fields = (self.update_fields, )


class Serializer(object):
    def __init__(self, data=None, initial=None):
        if data and not isinstance(data, dict):
            raise Exception('data needs to be a dictionary')
        self.data = data
        self.initial = initial or {}
        self.errors = {}

    def save(self):
        pass

    def validate_field(self, field, value, data):
        validation_name = 'validate_{}'.format(field)
        if hasattr(self, validation_name):
            validator = getattr(self, validation_name)
            validator(value)
        return None

    def _get_custom_field_serializers(self):
        """
        Get all custom serializer functions.
        If this function has a serializer attached to it, include that
        """
        functions = [(
            getattr(self, f),
            f.replace('serialize_', '')
        ) for f in dir(self) if f.startswith('serialize_')]
        return functions
