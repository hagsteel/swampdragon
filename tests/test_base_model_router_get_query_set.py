from swampdragon.route_handler import BaseModelRouter
from swampdragon.serializers.model_serializer import ModelSerializer
from swampdragon.testing.dragon_testcase import DragonTestCase
from .models import TextModel


class Serializer(ModelSerializer):
    class Meta:
        model = TextModel


class Router(BaseModelRouter):
    model = TextModel
    serializer_class = Serializer

    def get_query_set(self):
        return self.model.objects.all()


class TestBaseModelRouter(DragonTestCase):
    def test_get_query_set(self):
        TextModel.objects.create(text='This is a text model')

        router = Router(self.connection)
        with self.assertNumQueries(1):
            for i in range(2):
                router.get_list()
