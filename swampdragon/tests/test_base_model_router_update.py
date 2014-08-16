from ..route_handler import BaseModelRouter, SUCCESS, ERROR
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from swampdragon.tests.models import TwoFieldModel


class Serializer(ModelSerializer):
    class Meta:
        publish_fields = ('text', 'number')
        update_fields = ('text', 'number')
        model = TwoFieldModel


class Router(BaseModelRouter):
    model = TwoFieldModel
    serializer_class = Serializer

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])


class TestBaseModelRouter(DragonTestCase):
    def setUp(self):
        self.router = Router(self.connection)
        self.obj = self.router.model.objects.create(text='text', number=1)

    def test_successful_update(self):
        data = {'number': 3, 'id': self.obj.pk}
        self.router.update(**data)
        self.assertEqual(3, self.router.model.objects.get(pk=self.obj.pk).number)

    def test_error_on_update(self):
        data = {'text': None, 'id': self.obj.pk}
        self.router.update(**data)
        actual = self.connection.last_message
        self.assertEqual(actual['context']['state'], ERROR)
        self.assertIn('text', actual['data'])

    def test_updated(self):
        data = {'text': 'text', 'number': 3, 'id': self.obj.pk}
        self.router.update(**data)
        model = self.router.model.objects.get()
        actual = self.connection.last_message
        self.assertEqual(actual['context']['state'], SUCCESS)
        self.assertIn('number', actual['data'])
        self.assertNotIn('text', actual['data'])
