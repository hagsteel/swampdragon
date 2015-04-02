from swampdragon.route_handler import BaseRouter
from swampdragon.testing.dragon_testcase import DragonTestCase
from swampdragon.pubsub_providers.data_publisher import publish_data


class FooRouter(BaseRouter):
    def get_subscription_channels(self, **kwargs):
        return ['foo-chan']


class TestDataPublisher(DragonTestCase):
    def setUp(self):
        self.router = FooRouter(self.connection)
        self.router.subscribe(**{'channel': 'chan'})

    def test_publish_string(self):
        publish_data('foo-chan', 'hello')
        self.assertEqual(self.connection.last_pub['data'], 'hello')

    def test_publish_dict(self):
        publish_data('foo-chan', {'key': 'value'})
        self.assertEqual(self.connection.last_pub['data']['key'], 'value')
