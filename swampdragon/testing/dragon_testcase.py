from tornado.testing import AsyncHTTPTestCase
from tornado import netutil
from swampdragon import discover_routes
from swampdragon import route_handler
from swampdragon.pubsub_providers.subscriber_factory import get_subscription_provider
from swampdragon.connections.mock_connection import TestConnection
from django.test import TestCase
from django.conf import settings
from django.utils.importlib import import_module
from sockjs.tornado import SockJSRouter
from tornado import web
from swampdragon.settings_provider import SettingsHandler
import socket


pub_sub = get_subscription_provider()


def _bind_port(port=9988):
    [sock] = netutil.bind_sockets(port, 'localhost', family=socket.AF_INET)
    port = sock.getsockname()[1]
    return sock, port


class DragonTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        super(DragonTestCase, self).__init__(methodName)

        pub_sub._channels = []
        pub_sub._subscribers = {}
        self.connection = TestConnection()
        self.urls = discover_routes()

    def tearDown(self):
        pub_sub._channels = []
        pub_sub._subscribers = {}

    def _load_app(self):
        routers = []
        module_name, cls_name = settings.SWAMP_DRAGON_CONNECTION[0].rsplit('.', 1)
        module = import_module(module_name)
        cls = getattr(module, cls_name)
        channel = settings.SWAMP_DRAGON_CONNECTION[1]
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


class DragonTestCaseAsync(AsyncHTTPTestCase):
    def __init__(self, methodName='runTest'):
        super(DragonTestCaseAsync, self).__init__(methodName)

        pub_sub._channels = []
        pub_sub._subscribers = {}
        self.connection = TestConnection()
        self.urls = discover_routes()
        self.app = self._load_app()

    def setUp(self):
        super(AsyncHTTPTestCase, self).setUp()
        sock, port = _bind_port(getattr(self, 'port', 9988))
        self._port = port

        self.http_client = self.get_http_client()
        self._app = self.get_app()
        self.http_server = self.get_http_server()
        self.http_server.add_sockets([sock])

    def tearDown(self):
        route_handler.registered_handlers = {}
        pub_sub._channels = []
        pub_sub._subscribers = {}

    def get_http_port(self):
        return self._port

    def _load_app(self):
        routers = []
        module_name, cls_name = settings.SWAMP_DRAGON_CONNECTION[0].rsplit('.', 1)
        module = import_module(module_name)
        cls = getattr(module, cls_name)
        channel = settings.SWAMP_DRAGON_CONNECTION[1]
        routers.append(SockJSRouter(cls, channel))
        print('Channel {}'.format(channel))

        app_settings = {
            'debug': settings.DEBUG,
        }

        urls = discover_routes()
        for router in routers:
            urls += router.urls
        urls.append(('/settings.js$', SettingsHandler))

        app = web.Application(urls, **app_settings)
        return app

    def get_app(self):
        return self.app

    @property
    def host(self):
        return '{}://localhost:{}'.format(self.get_protocol(), self.get_http_port())
