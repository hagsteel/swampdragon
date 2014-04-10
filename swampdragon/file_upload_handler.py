from os.path import join
from os import makedirs
from django.conf import settings


def make_file_id(file_data):
    return str(abs(hash(file_data)))


def get_file_location(file_name, file_id):
    path = join(settings.MEDIA_ROOT, 'tmp')
    path = join(path, str(file_id))
    try:
        makedirs(path)
    except:
        pass
    return join(path, file_name)


def get_file_url(file_name, file_id):
    path = join(settings.MEDIA_URL, 'tmp')
    path = join(path, str(file_id))
    return join(path, file_name)
