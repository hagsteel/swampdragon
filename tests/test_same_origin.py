try:
    from http.cookies import SimpleCookie
except ImportError:
    from Cookie import SimpleCookie

from django.conf import settings
from sockjs.tornado.session import ConnectionInfo
from swampdragon.connections.sockjs_connection import SubscriberConnection
from swampdragon.testing.dragon_testcase import DragonTestCaseAsync
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


class TestSameOrigin(DragonTestCaseAsync):
    def test_same_origin(self):
        settings.DRAGON_URL = self.host
        settings.SWAMP_DRAGON_SAME_ORIGIN = True

        response = self.fetch('/settings.js')
        cookie = SimpleCookie(response.headers['Set-Cookie'])
        request = ConnectionInfo('127.0.0.1', cookies=cookie, arguments={}, headers={}, path='/data/983/9cz4ridg/websocket')
        session = TestSession()
        self.connection = SubscriberConnection(session)
        self.connection.on_open(request)

        self.assertFalse(self.connection.is_closed)
