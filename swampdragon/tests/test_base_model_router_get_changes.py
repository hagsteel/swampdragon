from ..route_handler import BaseModelRouter
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from swampdragon.tests.models import TwoFieldModel


class Serializer(ModelSerializer):
    class Meta:
        model = TwoFieldModel


class TestBaseModelRouter(DragonTestCase):
    def test_get_changes(self):
        router = BaseModelRouter(self.connection)
        router.serializer = Serializer(instance=TwoFieldModel())
        current_state = {'changed': 'updated', 'nochange': 123, 'id': 1}
        past_state = {'changed': 'foobar', 'nochange': 123, 'id': 1}
        changes = router._get_changes(current_state, past_state)
        expected = {'changed': 'updated', 'id': 1}
        self.assertDictEqual(changes, expected)
