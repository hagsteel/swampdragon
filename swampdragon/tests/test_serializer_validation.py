from ..serializers.model_serializer import ModelSerializer
from ..serializers.validation import ModelValidationError
from ..route_handler import ModelRouter, ERROR
from .. import route_handler
from .dragon_test_case import DragonTestCase
from .models import TwoFieldModel


class TwoFieldModelSerializer(ModelSerializer):
    class Meta:
        model = TwoFieldModel
        update_fields = ('text', 'number')

    def validate_text(self, val):
        if val == 'foo':
            raise ModelValidationError({'text': ['text error']})

    def validate_number(self, val):
        if val == 8:
            raise ModelValidationError({'number': ['number error']})


class Router(ModelRouter):
    valid_verbs = ('create', )
    route_name = 'validation-router'
    serializer_class = TwoFieldModelSerializer


class TestSerializerValidation(DragonTestCase):
    def test_validate_field(self):
        data = {'text': 'foo', 'number': 8}
        ser = TwoFieldModelSerializer(data)
        with self.assertRaises(ModelValidationError):
            ser.save()

    def test_validate_field_from_router(self):
        """
        Ensure that both the text and number error message
        is raised upon validation
        """
        data = {'text': 'foo', 'number': 8}
        route_handler.register(Router)
        self.connection.call_verb(Router.route_name, 'create', **data)
        self.assertEqual(self.connection.last_message['context']['state'], ERROR)
        self.assertIn('text', self.connection.last_message['data'])
        self.assertIn('number', self.connection.last_message['data'])
