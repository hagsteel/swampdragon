from ..route_handler import BaseRouter
from .dragon_test_case import DragonTestCase


class FooRouter(BaseRouter):
    valid_verbs = ('do_something', )
    route_name = 'foo'

    def get_client_context(self, verb, **kwargs):
        context = super(FooRouter, self).get_client_context(verb, **kwargs)
        context['extra'] = 'value'
        return context

    def do_something(self, **kwargs):
        self.send({'foo': 'bar'})


class TestBaseRouter(DragonTestCase):
    def setUp(self):
        self.router = FooRouter(self.connection)

    def test_get_client_context(self):
        data = {'verb': 'do_something'}
        self.router.handle(data)

        message = self.connection.last_message
        client_context = message['context']['client_context']
        self.assertDictEqual(client_context, self.router.get_client_context('do_something'))

    def test_empty_client_context(self):
        self.assertIsNone(self.router._update_client_context(None))
