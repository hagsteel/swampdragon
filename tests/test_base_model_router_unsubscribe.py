from swampdragon.route_handler import BaseModelRouter, SUCCESS
from swampdragon.serializers.model_serializer import ModelSerializer
from swampdragon.testing.dragon_testcase import DragonTestCase
from .models import TwoFieldModel


class Serializer(ModelSerializer):
    class Meta:
        update_fields = ('text', 'number')
        model = TwoFieldModel


class Router(BaseModelRouter):
    model = TwoFieldModel
    serializer_class = Serializer


class TestBaseModelRouter(DragonTestCase):
    def setUp(self):
        self.router = Router(self.connection)

    def test_unsubscribe(self):
        data = {'channel': 'client-channel'}
        self.router.unsubscribe(**data)
        self.assertEqual(self.connection.last_message['context']['state'], SUCCESS)
        self.assertEqual(self.connection.last_message['data'], 'unsubscribed')
