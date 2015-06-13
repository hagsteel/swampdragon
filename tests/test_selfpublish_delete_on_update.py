from swampdragon.route_handler import ModelRouter
from swampdragon.testing.dragon_testcase import DragonTestCase
from swampdragon.connections.mock_connection import TestConnection
from .models import FooSelfPub
from .serializers import FooSelfPubSerializer


class FooModelRouter(ModelRouter):
    serializer_class = FooSelfPubSerializer


class TestSelfPubModel(DragonTestCase):
    def test_self_pub_model(self):
        connection = TestConnection()

        foo_a = FooSelfPub.objects.create(name='test a', number=123)
        foo_b = FooSelfPub.objects.create(name='test b', number=456)
        router = FooModelRouter(connection)
        router.subscribe(channel='testchan', number=foo_a.number)
        foo_a.name = 'updated'
        foo_a.save()
        foo_b.name = 'updated'
        foo_b.save()

        pd = connection.published_data
        self.assertEqual(len(pd), 1)

        #  Change the number, thus the model no longer match the filter
        #  this should trigger a delete message
        foo_a.number = 1
        foo_a.save()
        self.assertEqual(connection.last_pub['action'], 'deleted')
