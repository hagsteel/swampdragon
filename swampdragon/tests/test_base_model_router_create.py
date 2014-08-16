from ..route_handler import BaseModelRouter, SUCCESS, ERROR
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

    def test_successful_create(self):
        data = {'text': 'text', 'number': 3}
        self.router.create(**data)
        model = self.router.model.objects.get()
        self.assertIsNotNone(model)

    def test_error_on_create(self):
        data = {'text': 'text'}
        self.router.create(**data)
        actual = self.connection.last_message
        self.assertEqual(actual['context']['state'], ERROR)
        self.assertIn('number', actual['data'])

    def test_created(self):
        data = {'text': 'text', 'number': 3}
        self.router.create(**data)
        model = self.router.model.objects.get()
        actual = self.connection.last_message
        self.assertEqual(actual['context']['state'], SUCCESS)
        self.assertDictEqual(actual['data'], Serializer(instance=model).serialize())
