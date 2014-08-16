from ..route_handler import BaseModelRouter, SUCCESS
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from swampdragon.tests.models import TwoFieldModel


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

    def test_subscribe(self):
        data = {'channel': 'client-channel'}
        self.router.subscribe(**data)
        self.assertEqual(self.connection.last_message['context']['state'], SUCCESS)
        self.assertIn('channel_data', self.connection.last_message)
        self.assertEqual(self.connection.last_message['channel_data']['local_channel'], 'client-channel')
