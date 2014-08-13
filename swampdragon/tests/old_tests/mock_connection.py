import json
import uuid
from .mock_provider import MockPubSubProvider
from .. import route_handler


class TestConnection(object):
    uid = None

    def __init__(self, user=None):
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
        if not isinstance(data, dict):
            data = json.loads(data)
        handler = route_handler.get_route_handler(data['route'])
        handler(self).handle(data)

    def call_verb(self, route, verb, **kwargs):
        self.client_send({
            'route': route,
            'verb': verb,
            'args': kwargs
        })
        return self.get_last_message()

    def get_user(self, **kwargs):
        return self.user

    def get_last_message(self):
        if not self.sent_data:
            return None
        last_message = self.sent_data[-1]
        if not isinstance(last_message, dict):
            last_message = json.loads(last_message)
        return last_message

    def get_last_published(self):
        if not self.published_data:
            return None
        if isinstance(self.published_data[-1], dict):
            return self.published_data[-1]
        return json.loads(self.published_data[-1])

    def get_last_published_data(self):
        last_pub = self.get_last_published()
        if last_pub is None:
            return None
        return last_pub['data']

    def subscribe(self, route, client_channel, subscription_data):
        data = {'route': route, 'verb': 'subscribe', 'args': {'channel': client_channel}}
        data['args'].update(subscription_data)
        self.client_send(data)

    def unsubscribe(self, route, client_channel, subscription_data):
        data = {'route': route, 'verb': 'unsubscribe', 'args': {'channel': client_channel}}
        data['args'].update(subscription_data)
        self.client_send(data)

    def create(self, route, data):
        self.client_send({'route': route, 'verb': 'create', 'args': data})

    def update(self, route, data):
        self.client_send({'route': route, 'verb': 'update', 'args': data})

    def remove(self, route, data):
        self.client_send({'route': route, 'verb': 'delete', 'args': data})
