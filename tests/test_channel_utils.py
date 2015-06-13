from swampdragon.pubsub_providers.channel_utils import properties_match_channel_by_object, properties_match_channel_by_dict
from swampdragon.testing.dragon_testcase import DragonTestCase
from .models import FooSelfPub


class TestSelfPubModel(DragonTestCase):
    def test_self_pub_model(self):
        channel_props = [('name__contains', 'findme')]
        foo = FooSelfPub.objects.create(name='findme')
        dict = {'name': 'findme'}
        x = properties_match_channel_by_object(foo, channel_props)
        y = properties_match_channel_by_dict(dict, channel_props)
        self.assertTrue(x)
        self.assertTrue(y)
