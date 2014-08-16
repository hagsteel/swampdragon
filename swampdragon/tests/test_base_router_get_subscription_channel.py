from ..route_handler import BaseRouter, ERROR, SUCCESS, LOGIN_REQUIRED
from .dragon_test_case import DragonTestCase


class FooRouter(BaseRouter):
    route_name = 'foo'


class BarRouter(BaseRouter):
    channels = ['channel_a', 'channel_b']

    def get_subscription_channels(self, **kwargs):
        return self.channels


class TestBaseRouter(DragonTestCase):
    def setUp(self):
        self.foo_router = FooRouter(self.connection)
        self.bar_router = BarRouter(self.connection)

    def test_get_subscription_channel(self):
        with self.assertRaises(NotImplementedError):
            self.foo_router.get_subscription_channels()

        channel = self.bar_router.get_subscription_channels()
        self.assertListEqual(channel, BarRouter.channels)
