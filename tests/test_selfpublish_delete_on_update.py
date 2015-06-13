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

        foo_a = FooSelfPub.objects.create(name='test a')
        foo_b = FooSelfPub.objects.create(name='test b')
        router = FooModelRouter(connection)
        router.subscribe(channel='testchan', id=foo_a.id)
        foo_a.name = 'updated'
        foo_a.save()
        foo_b.name = 'updated'
        foo_b.save()

        pd = connection.published_data
        self.assertEqual(len(pd), 1)
