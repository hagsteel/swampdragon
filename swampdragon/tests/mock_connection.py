import json
import uuid
from django.contrib.auth.models import AnonymousUser
from .mock_provider import MockPubSubProvider
from .models import TestUser
from .. import route_handler
from ..connections.sockjs_connection import ConnectionMixin


class TestConnection(ConnectionMixin):
    uid = None

    def __init__(self, user=AnonymousUser()):
        self.uid = str(uuid.uuid4())
        self.user = user

        self.sent_data = []
        self.published_data = []
        self.pub_sub = MockPubSubProvider()

    def send(self, message):
        self.sent_data.append(json.dumps(message))

    def publish(self, message):
        self.published_data.append(json.dumps(message))

    def client_send(self, data):
        data = self.to_json(data)
        handler = route_handler.get_route_handler(data['route'])
        handler(self).handle(data)

    def get_user(self, **kwargs):
        return self.user

    def get_last_message(self):
        if not self.sent_data:
            return None
        return self.to_json(self.sent_data[-1])

    def get_last_data(self):
        if not self.sent_data:
            return None
        data = self.to_json(self.sent_data[-1])
        if 'data' in data and data['data']:
            return data['data']
        return None


class TestConnectionWithUser(TestConnection):
    def __init__(self, user=None):
        super(TestConnectionWithUser, self).__init__()
        if user is None:
            self.user = TestUser()
        else:
            self.user = user

    def get_user(self, **kwargs):
        return self.user
