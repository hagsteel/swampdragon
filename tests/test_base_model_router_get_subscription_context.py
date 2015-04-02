from swampdragon.route_handler import BaseModelRouter
from swampdragon.serializers.model_serializer import ModelSerializer
from swampdragon.testing.dragon_testcase import DragonTestCase
from .models import TwoFieldModel


class Serializer(ModelSerializer):
    class Meta:
        model = TwoFieldModel


class Router(BaseModelRouter):
    model = TwoFieldModel
    serializer_class = Serializer

    def get_subscription_contexts(self, **kwargs):
        context = super(Router, self).get_subscription_contexts(**kwargs)
        context['key'] = 'val'
        return context


class TestBaseModelRouter(DragonTestCase):
    def setUp(self):
        self.router = Router(self.connection)

    def test_get_subscription_context(self):
        actual = self.router.get_subscription_contexts()
        expected = {'key': 'val'}
        self.assertDictEqual(actual, expected)
