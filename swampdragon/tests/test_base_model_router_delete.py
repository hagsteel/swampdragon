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

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])


class TestBaseModelRouter(DragonTestCase):
    def setUp(self):
        self.router = Router(self.connection)
        self.obj = self.router.model.objects.create(text='text', number=1)

    def test_successful_delete(self):
        data = {'id': self.obj.pk}
        self.router.delete(**data)
        self.assertFalse(self.router.model.objects.exists())

    def test_deleted(self):
        data = {'id': self.obj.pk}
        self.router.delete(**data)
        actual = self.connection.last_message
        self.assertEqual(actual['context']['state'], SUCCESS)
        self.assertEqual(actual['data']['id'], data['id'])
