from swampdragon.route_handler import ModelRouter
from swampdragon.testing.dragon_testcase import DragonTestCase
from .models import BoolSelfPub
from .serializers import BoolSelfPubSerializer


class BoolSelfPubRouter(ModelRouter):
    serializer_class = BoolSelfPubSerializer


class TestSelfPubModel(DragonTestCase):
    def test_self_pub_model_bool_change(self):
        router = BoolSelfPubRouter(self.connection)
        router.subscribe(**{'channel': 'testchan'})
        self.assertIsNone(self.connection.last_pub)
        model = BoolSelfPub.objects.create(bool=True)
        self.assertIsNotNone(self.connection.last_pub)
        self.assertEqual(len(self.connection.published_data), 1)
        model.bool = False
        model.save()
        self.assertEqual(len(self.connection.published_data), 2)
        model.bool = True
        model.save()
        self.assertEqual(len(self.connection.published_data), 3)
