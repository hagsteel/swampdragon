from ..route_handler import BaseModelPublisherRouter, SUCCESS, ERROR
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from swampdragon.tests.models import TwoFieldModel


class Serializer(ModelSerializer):
    class Meta:
        publish_fields = ('id')
        update_fields = ('text', 'number')
        model = TwoFieldModel


class Router(BaseModelPublisherRouter):
    model = TwoFieldModel
    serializer_class = Serializer

    def get_object(self, **kwargs):
        return self.model.objects.get(**kwargs)


class TestBaseModelPublisherRouter(DragonTestCase):
    def setUp(self):
        self.router = Router(self.connection)
        self.obj = self.router.model.objects.create(text='text', number=5)

    def test_deleted(self):
        data = {'id': self.obj.pk}
        self.router.subscribe(**{'channel': 'client-channel'})
        self.router.delete(**data)
        actual = self.connection.get_last_published()
        expected = {'action': 'deleted', 'channel': 'twofieldmodel|', 'data': {'_type': 'twofieldmodel', 'id': 1}}
        self.assertDictEqual(actual, expected)
