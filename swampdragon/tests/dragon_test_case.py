from django.test import TestCase
from django.conf import settings
from django.utils.importlib import import_module
from sockjs.tornado import SockJSRouter
from tornado import web
from .. import discover_routes
from .. import route_handler
from ..pubsub_providers.pubsub_factory import get_subscription_provider
from .mock_connection import TestConnection


pub_sub = get_subscription_provider()


class DragonTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        super(DragonTestCase, self).__init__(methodName)
        pub_sub._channels = []
        pub_sub._subscribers = {}
        self.connection = TestConnection()
        self.urls = discover_routes()

    def tearDown(self):
        route_handler.registered_handlers = {}
        pub_sub._channels = []
        pub_sub._subscribers = {}

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
