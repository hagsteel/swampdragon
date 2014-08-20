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
        current_state = {'changed': 'a', 'nochange': 123, 'id': 1}
        past_state = {'changed': 'b', 'nochange': 123, 'id': 1}
        changed_fields = router._get_changed_fields(current_state, past_state)
        expected = ['changed']
        self.assertListEqual(expected, changed_fields)
