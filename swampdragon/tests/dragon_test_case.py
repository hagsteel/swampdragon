from unittest import TestCase
from . import mock_provider
from django.conf import settings
from django.utils.importlib import import_module
from sockjs.tornado import SockJSRouter
from tornado import web, ioloop
from swampdragon import discover_routes
from swampdragon.models import SelfPublishModel
from swampdragon.tests.mock_connection import TestConnection
from swampdragon.tests.mock_provider import MockPubSubProvider


class DragonTestCase(TestCase):
    is_patched = False

    def __init__(self, methodName='runTest'):
        super(DragonTestCase, self).__init__(methodName)
        self.patch_pubsub()
        mock_provider._channels = []
        mock_provider._subscribers = {}
        self.connection = TestConnection()
        self.urls = discover_routes()

    def tearDown(self):
        mock_provider._channels = []
        mock_provider._subscribers = {}

    def patch_pubsub(self):
        if self.is_patched:
            return
        SelfPublishModel.publisher_class = MockPubSubProvider
        self.is_patched = True

    def _load_app(self):
        routers = []
        for sockjs_class in settings.SOCKJS_CLASSES:
            module_name, cls_name = sockjs_class[0].rsplit('.', 1)
            module = import_module(module_name)
            cls = getattr(module, cls_name)
            channel = sockjs_class[1]
            routers.append(SockJSRouter(cls, channel))
            print('Channel {}'.format(channel))

        app_settings = {
            'debug': settings.DEBUG,
        }

        urls = discover_routes()
        for router in routers:
            urls += router.urls

        app = web.Application(urls, **app_settings)
        return app
