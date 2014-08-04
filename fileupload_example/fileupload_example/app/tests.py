import json
import tempfile
from PIL import Image
import tornado
from tornado.testing import AsyncHTTPTestCase, bind_unused_port
from .models import WithFile, MultiFileModel, File
from swampdragon.tests.dragon_django_test_case import DragonDjangoTestCase, FileUploadRequestData

from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio

AsyncIOMainLoop().install()


class SelfPubExampleTest(DragonDjangoTestCase, AsyncHTTPTestCase):
    def setUp(self):
        super(SelfPubExampleTest, self).setUp()
        self.as_client = self.get_http_client()
        self.upload_url = self.get_url('/_sdfileupload/')

    def get_app(self):
        return self._load_app()

    def _generate_image_file(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        return tmp_file

    def _generate_text_file(self):
        tmp_file = tempfile.NamedTemporaryFile(suffix='.txt')
        seq = [b'Hello\nWorld']
        tmp_file.file.writelines(seq)
        tmp_file.file.seek(0)
        return tmp_file

    @tornado.testing.gen_test
    def test_get_request_fileupload(self):
        url = self.get_url('/_sdfileupload/')
        self.as_client = self.get_http_client()
        response = yield self.as_client.fetch(self.upload_url, method='GET')
        self.assertEqual(response.body.decode(), 'Hello!')

    @tornado.testing.gen_test
    def test_single_file_upload(self):
        tmp_text_file = self._generate_text_file()
        fur = FileUploadRequestData([tmp_text_file])
        response = yield self.as_client.fetch(self.upload_url, method='POST', body=fur.get_body(),
                                              headers=fur.get_headers())
        data = json.loads(response.body.decode())
        self.assertEqual(data['files'][0]['file_name'], tmp_text_file.name.split('/')[-1])

    @tornado.testing.gen_test
    def test_multiple_file_upload(self):
        tmp_text_file = self._generate_text_file()
        tmp_img_file = self._generate_image_file()
        fur = FileUploadRequestData([tmp_text_file, tmp_img_file])
        response = yield self.as_client.fetch(self.upload_url, method='POST', body=fur.get_body(),
                                              headers=fur.get_headers())
        data = json.loads(response.body.decode())

    @tornado.testing.gen_test
    def test_create_with_file(self):
        tmp_text_file = self._generate_text_file()
        fur = FileUploadRequestData([tmp_text_file])
        response = yield self.as_client.fetch(self.upload_url, method='POST', body=fur.get_body(),
                                              headers=fur.get_headers())
        file_data = json.loads(response.body.decode())
        data = {
            'name': 'foo',
            'file': [file_data['files'][0]]
        }
        self.connection.call_verb('withfile-route', 'create', **data)
        last_data = self.connection.get_last_message()['data']
        self.assertGreater(len(last_data['file']), 0)

    @tornado.testing.gen_test
    def test_create_with_multiple_files(self):
        tmp_text_file = self._generate_text_file()
        tmp_img_file = self._generate_image_file()
        fur = FileUploadRequestData([tmp_text_file, tmp_img_file])
        response = yield self.as_client.fetch(self.upload_url, method='POST', body=fur.get_body(),
                                              headers=fur.get_headers())
        file_data = json.loads(response.body.decode())
        data = {
            'text': 'foo',
            'files': [{'file': f} for f in file_data['files']]
        }

        self.connection.call_verb('multifile-route', 'create', **data)
        last_data = self.connection.get_last_message()['data']
        self.assertEqual(len(last_data['files']), 2)
