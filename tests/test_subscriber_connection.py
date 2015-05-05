from sockjs.tornado.session import ConnectionInfo
from swampdragon.connections.sockjs_connection import SubscriberConnection
from swampdragon.route_handler import BaseRouter, UnexpectedVerbException
from swampdragon.testing.dragon_testcase import DragonTestCase
from swampdragon import route_handler
import uuid


class TestSession(object):
    def __init__(self, is_open=True):
        self.session_id = uuid.uuid4().hex
        self.is_closed = is_open is False
        self.messages = []

    def send_message(self, message, binary=False):
        self.messages.append(message)

    def close(self, code=3000, message='Connection closed'):
        self.is_closed = True


class TestRouter(BaseRouter):
    route_name = 'test-router'
    valid_verbs = ['say_hello']

    def say_hello(self, **kwargs):
        self.connection.hello_said = True


class TestSubscriberConnection(DragonTestCase):
    def setUp(self):
        self.session = TestSession()
        self.connection = SubscriberConnection(self.session)

    def test_on_close(self):
        """
        Closing a connection should automatically unsubscribe
        from all channels
        """
        request = ConnectionInfo('127.0.0.1', cookies={}, arguments={}, headers={}, path='/data/983/9cz4ridg/websocket')
        self.connection.on_open(request)
        self.connection.pub_sub.subscribe(['test-channel'], self.connection)
        self.assertIn(self.connection, self.connection.pub_sub.publisher.subscribers['test-channel'])
        self.connection.on_close()
        self.assertNotIn('test-channel', self.connection.pub_sub.publisher.subscribers)

    def test_on_message(self):
        route_handler.register(TestRouter)
        data = {'verb': 'say_hello', 'route': TestRouter.get_name()}
        self.connection.on_message(data)
        self.assertTrue(self.connection.hello_said)

    def test_on_message_invalid_verb(self):
        route_handler.register(TestRouter)
        data = {'verb': 'invalid_verb', 'route': TestRouter.get_name()}
        with self.assertRaises(UnexpectedVerbException):
            self.connection.on_message(data)
        self.assertTrue(self.connection.is_closed)

    def test_string_to_json(self):
        data = '{"key": "val"}'
        self.assertDictEqual({'key': 'val'}, self.connection.to_json(data))

    def test_to_json_plain_text(self):
        expected = {'message': 'hello'}
        self.assertDictEqual(expected, self.connection.to_json('hello'))

    def test_dict_to_json(self):
        """
        If the message received is a dictionary simply return it
        """
        expected = {'key': 'value'}
        actual = self.connection.to_json(expected)
        self.assertEqual(expected, actual)
