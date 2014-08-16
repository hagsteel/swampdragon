from django.test import TestCase
from mimetypes import MimeTypes
from swampdragon.tests.dragon_test_case import DragonTestCase


# class DragonDjangoTestCase(DragonTestCase, TestCase):
#     pass


class FileUploadRequestData(object):
    def __init__(self, files):
        if not isinstance(files, list):
            files = [files]
        self.boundary = '--dragontestclient'
        self.body = ''
        for f in files:
            self.add_file(f)
        self.close_body()

    def get_headers(self):
        return {
            'Accept-Language': 'en-US,en;q=0.8',
            'Content-Length': '{}'.format(len(self.get_body())),
            'Origin': '/',
            'Content-Type': 'multipart/form-data; boundary={}'.format(self.boundary),
        }

    def add_file(self, file):
        mime = MimeTypes()
        mime_type = mime.guess_type(file.name)[0]
        data = {
            'file': file,
            'boundary': self.boundary,
            'mimetype': mime_type,
            'filename': file.name.split('/')[-1],
            'file_body': file.read().decode()
        }
        self.body += '--{boundary}\r\n\r\n'.format(**data)
        self.body += 'Content-Disposition: form-data; name="uploadedFile"; filename="{filename}"\r\n'.format(**data)
        self.body += 'Content-Type: {mimetype}\r\n\r\n'.format(**data)
        self.body += '{file_body}'.format(**data)
        self.body += '\r\n'

    def close_body(self):
        self.body += '--{}--\r\n\r\n'.format(self.boundary)

    def get_body(self):
        return self.body
