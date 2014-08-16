from ..route_handler import BaseRouter, ERROR, SUCCESS, LOGIN_REQUIRED
from .dragon_test_case import DragonTestCase


class FooRouter(BaseRouter):
    route_name = 'foo'


class TestBaseRouter(DragonTestCase):
    def setUp(self):
        self.router = FooRouter(self.connection)

    def test_send(self):
        message = 'today is a good day'
        self.router.send(message)
        self.assertEqual(self.connection.last_message['data'], message)
        self.assertEqual(self.connection.last_message['context']['state'], SUCCESS)

    def test_send_error(self):
        error = "it's gone wrong"
        self.router.send_error(error)
        self.assertEqual(self.connection.last_message['data'], error)
        self.assertEqual(self.connection.last_message['context']['state'], ERROR)

    def test_login_required(self):
        self.router.send_login_required()
        self.assertEqual(self.connection.last_message['context']['state'], LOGIN_REQUIRED)
