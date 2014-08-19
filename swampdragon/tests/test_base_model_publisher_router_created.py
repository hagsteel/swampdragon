from ..route_handler import BaseModelPublisherRouter, SUCCESS, ERROR
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from swampdragon.tests.models import TwoFieldModel


class Serializer(ModelSerializer):
    class Meta:
        publish_fields = ('id',)
        update_fields = ('text', 'number')
        model = TwoFieldModel


class Router(BaseModelPublisherRouter):
    model = TwoFieldModel
    serializer_class = Serializer


class TestBaseModelPublisherRouter(DragonTestCase):
    def setUp(self):
        self.router = Router(self.connection)

    def test_created(self):
        data = {'text': 'text', 'number': 3}
        self.router.create(**data)
        model = self.router.model.objects.get()
        self.assertIsNotNone(model)

    def test_created_publish(self):
        self.router.subscribe(**{'channel': 'client-channel'})
        data = {'text': 'text', 'number': 3}
        self.router.create(**data)
        actual = self.connection.last_pub
        expected = {'action': 'created', 'channel': 'twofieldmodel|', 'data': {'_type': 'twofieldmodel', 'id': 1}}
        self.assertDictEqual(actual, expected)
