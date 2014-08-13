from .dragon_django_test_case import DragonDjangoTestCase
from swampdragon import route_handler
from swampdragon.serializers.validation import ModelValidationError
from swampdragon.tests.serializers import FooSerializer
from swampdragon.tests.test_route_handler import FooRouter


class ValidationTest(DragonDjangoTestCase):
    def setUp(self):
        route_handler.register(FooRouter)

    def test_trigger_validation_error(self):
        data = {'test_field_a': 'missing field b'}
        with self.assertRaises(ModelValidationError):
            FooSerializer(data=data).save()

    def test_router_validation_error(self):
        data = {'test_field_a': 'missing field b'}
        self.connection.call_verb('test_parent_router', 'create', **data)
        message = self.connection.get_last_message()
        self.assertEqual('error', message['context']['state'])
