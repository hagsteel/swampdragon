from os.path import join
from os import makedirs
from django.conf import settings
from datetime import datetime
import time


def make_file_id(file_data):
    timestamp = datetime.now()
    timestamp = time.mktime(timestamp.timetuple()) * 1e3 + timestamp.microsecond / 1e3
    timestamp = '{}'.format(timestamp).encode()
    return str(abs(hash(file_data + timestamp)))


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
