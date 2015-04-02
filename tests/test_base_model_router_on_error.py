from swampdragon.route_handler import BaseModelRouter
from swampdragon.serializers.model_serializer import ModelSerializer
from swampdragon.testing.dragon_testcase import DragonTestCase
from .models import TwoFieldModel


class Serializer(ModelSerializer):
    class Meta:
        model = TwoFieldModel


class TestBaseModelRouter(DragonTestCase):
    def setUp(self):
        self.router = BaseModelRouter(self.connection)

    def test_on_error(self):
        self.router.on_error({'key': 'error'})
        actual = self.connection.last_message
        expected = {'context': {'state': 'error'}, 'data': {'key': 'error'}}
        self.assertDictEqual(actual, expected)
