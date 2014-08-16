from ..route_handler import BaseModelRouter
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import TwoFieldModel


class Serializer(ModelSerializer):
    class Meta:
        model = TwoFieldModel


class Router(BaseModelRouter):
    model = TwoFieldModel
    serializer_class = Serializer


class TestBaseModelRouter(DragonTestCase):
    def setUp(self):
        self.router = Router(self.connection)
        for i in range(5):
            TwoFieldModel.objects.create(text='text {}'.format(i), number=i)

    def test_send_list(self):
        qs = self.router.model.objects.all()
        self.router.send_list(qs)
        actual = self.connection.last_message['data']
        expected = [Serializer(instance=o).serialize() for o in qs]
        self.assertListEqual(actual, expected)
