from ..route_handler import BaseRouter
from .dragon_test_case import DragonTestCase


class FooRouter(BaseRouter):
    route_name = 'foo'

    def get_subscription_channels(self, **kwargs):
        channel = 'foo-{}'.format(kwargs['value'])
        return [channel]


class TestBaseRouter(DragonTestCase):
    def setUp(self):
        self.router = FooRouter(self.connection)

    def test_subscribe(self):
        data = {
            'value': 'bar',
            'channel': 'client-channel'
        }
        self.router.subscribe(**data)
        self.assertEqual(self.connection.last_message['data'], 'subscribed')
        self.assertListEqual(self.connection.last_message['channel_data']['remote_channels'], ['foo-bar'])

    def test_unsubscribe(self):
        data = {
            'value': 'bar',
            'channel': 'client-channel'
        }
        self.router.unsubscribe(**data)
        self.assertEqual(self.connection.last_message['data'], 'unsubscribed')
        self.assertListEqual(self.connection.last_message['channel_data']['remote_channels'], ['foo-bar'])
