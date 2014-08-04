from django.core.files import File
from django.core.files.base import ContentFile
from dateutil.parser import parse
from ..route_handler import get_file_location


class BaseDeserializer(object):
    def __call__(self, *args, **kwargs):
        raise NotImplemented()


class FileDeserializer(BaseDeserializer):
    def __call__(self, model_instance, key, val):
        if not val:
            return
        if isinstance(val, str):
            return
        import ipdb;ipdb.set_trace()
        file_id = int(val['file_id'])
        if not file_id > 0:
            return
        path = get_file_location(val['file_name'], val['file_id'])
        uploaded_file = File(open(path, 'rb'))
        setattr(model_instance, key, val['file_name'])
        getattr(model_instance, key).save(
            val['file_name'],
            ContentFile(uploaded_file.read()),
            save=False
        )


class ImageDeserializer(FileDeserializer):
    pass


class DateTimeDeserializer(BaseDeserializer):
    def __call__(self, model_instance, key, val):
        date_val = parse(val)
        setattr(model_instance, key, date_val)


class DateDeserializer(DateTimeDeserializer):
    pass


deserializer_map = {
    'FileField': FileDeserializer,
    'ImageField': ImageDeserializer,
    'DateTimeField': DateTimeDeserializer,
    'DateField': DateDeserializer,
}

def get_deserializer(name):
    if name in deserializer_map:
        return deserializer_map[name]()
    return None