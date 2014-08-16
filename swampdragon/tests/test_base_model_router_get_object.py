from ..route_handler import BaseModelRouter
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from swampdragon.tests.models import TextModel


class Serializer(ModelSerializer):
    class Meta:
        model = TextModel


class Router(BaseModelRouter):
    model = TextModel
    serializer_class = Serializer

    def get_object(self, **kwargs):
        return self.model.objects.first()


class TestBaseModelRouter(DragonTestCase):
    def test_get_object(self):
        TextModel.objects.create(text='This is a text model')

        router = Router(self.connection)
        with self.assertNumQueries(1):
            for i in range(2):
                router.get_single()
