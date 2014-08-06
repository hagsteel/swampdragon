from dateutil.parser import parse


deserializer_map = {}


def register_field_deserializer(field_name, deserializer):
    deserializer_map[field_name] = deserializer


class BaseFieldDeserializer(object):
    def __call__(self, *args, **kwargs):
        raise NotImplemented()


class DateTimeDeserializer(BaseFieldDeserializer):
    def __call__(self, model_instance, key, val):
        date_val = parse(val)
        setattr(model_instance, key, date_val)


class DateDeserializer(DateTimeDeserializer):
    pass


register_field_deserializer('DateTimeField', DateTimeDeserializer)
register_field_deserializer('DateField', DateDeserializer)


def get_deserializer(name):
    if name in deserializer_map:
        return deserializer_map[name]()
    return None
