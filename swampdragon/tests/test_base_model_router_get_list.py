from ..serializers.model_serializer import ModelSerializer
from ..route_handler import BaseModelRouter
from .dragon_test_case import DragonTestCase
from .models import TextModel


class FooModelSerializer(ModelSerializer):
    class Meta:
        model = TextModel
        publish_fields = ('text', )


class FooRouter(BaseModelRouter):
    route_name = 'foo'
    valid_verbs = ('get_list', )
    model = TextModel
    serializer_class = FooModelSerializer

    def get_query_set(self, **kwargs):
        return self.model.objects.all()


class TestBaseModelRouter(DragonTestCase):
    def test_get_list(self):
        TextModel.objects.create(text='foo bar')
        foos = FooRouter(self.connection).get_list()
        self.assertListEqual(list(foos), list(TextModel.objects.all()))
