from ..route_handler import BaseModelRouter
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import TwoFieldModel


class FooSerializer(ModelSerializer):
    class Meta:
        model = TwoFieldModel
        publish_fields = ('text', 'number')
        update_fields = ('text', )


class FooRouter(BaseModelRouter):
    route_name = 'foo'
    model = TwoFieldModel
    serializer_class = FooSerializer

    def get_initial(self, verb, **kwargs):
        initial = super(FooRouter, self).get_initial(verb, **kwargs)
        initial['number'] = 123
        return initial


class TestBaseModelRouter(DragonTestCase):
    def setUp(self):
        self.router = FooRouter(self.connection)

    def test_get_initial_data(self):
        data = {'text': 'foo bar'}
        self.router.create(**data)
        object = TwoFieldModel.objects.get()
        self.assertEqual(object.number, 123)
