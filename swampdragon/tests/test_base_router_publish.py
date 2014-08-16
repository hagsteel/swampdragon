from ..route_handler import BaseRouter
from .dragon_test_case import DragonTestCase


class FooRouter(BaseRouter):
    route_name = 'foo'

    def get_subscription_channels(self, **kwargs):
        return ['foo-chan']


class TestBaseRouter(DragonTestCase):
    def setUp(self):
        self.router = FooRouter(self.connection)

    def test_publish(self):
        data = {'channel': 'foo'}
        self.router.subscribe(**data)
        self.router.publish(['foo-chan'], {'key': 'value'})
        actual = self.connection.get_last_published()
        expected = {'key': 'value', 'channel': 'foo-chan'}
        self.assertDictEqual(actual, expected)
