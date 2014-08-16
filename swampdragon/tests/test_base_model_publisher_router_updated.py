from ..route_handler import BaseModelPublisherRouter, SUCCESS, ERROR
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from swampdragon.tests.models import TwoFieldModel


class Serializer(ModelSerializer):
    class Meta:
        publish_fields = ('text', 'number')
        update_fields = ('text', 'number')
        model = TwoFieldModel


class Router(BaseModelPublisherRouter):
    model = TwoFieldModel
    serializer_class = Serializer

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

class TestBaseModelPublisherRouter(DragonTestCase):
    def setUp(self):
        self.router = Router(self.connection)
        self.obj = self.router.model.objects.create(text='text', number=123)

    def test_updated(self):
        data = {'text': 'text', 'number': 3, 'id': self.obj.pk}
        self.router.update(**data)
        model = self.router.model.objects.get()
        self.assertEqual(model.number, data['number'])

    def test_updated_publish(self):
        self.router.subscribe(**{'channel': 'client-channel'})
        data = {'text': 'text', 'number': 3, 'id': self.obj.pk}
        self.router.update(**data)
        actual = self.connection.get_last_published()
        expected = {'action': 'updated', 'channel': 'twofieldmodel|', 'data': {'_type': 'twofieldmodel', 'id': 1, 'number': 3}}
        self.assertDictEqual(actual, expected)
