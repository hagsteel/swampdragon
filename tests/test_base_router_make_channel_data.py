from swampdragon.pubsub_providers.base_provider import PUBACTIONS
from swampdragon.route_handler import BaseRouter
from swampdragon.testing.dragon_testcase import DragonTestCase


class FooRouter(BaseRouter):
    pass


class TestBaseRouter(DragonTestCase):
    def test_get_list(self):
        channel_data = FooRouter(self.connection).make_channel_data('client_chan', 'server_chan', action=PUBACTIONS.created)
        expected = {'local_channel': 'client_chan', 'remote_channels': 'server_chan', 'action': PUBACTIONS.created}
        self.assertDictEqual(channel_data, expected)
