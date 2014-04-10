import dateutil
from django.core.files import File
from os.path import join
from django.core.files.base import ContentFile
from dateutil.parser import parse


class BaseDeserializer(object):
    def __call__(self, *args, **kwargs):
        raise NotImplemented()


class FileDeserializer(BaseDeserializer):
    def __call__(self, model_instance, key, val):
        file_id = int(val['file_id'])
        if not file_id > 0:
            return

        path = join('/tmp', str(file_id))
        full_path = join(path, val['file_name'])
        uploaded_file = File(file(full_path))
        setattr(model_instance, key, val['file_name'])
        getattr(model_instance, key).save(
            val['file_name'],
            ContentFile(uploaded_file.read()),
            save=True
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