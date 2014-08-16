from ..route_handler import BaseRouter, UnexpectedVerbException
from .dragon_test_case import DragonTestCase
from swampdragon.permissions import RoutePermission


class FooRouter(BaseRouter):
    valid_verbs = ('call_foo')
    route_name = 'foo'
    router_called = False

    def call_foo(self, **kwargs):
        self.router_called = True


class Permission(RoutePermission):
    def test_permission(self, handler, verb, **kwargs):
        return kwargs['permission_pass']

    def permission_failed(self, handler):
        pass


class TestBaseRouter(DragonTestCase):
    def setUp(self):
        self.router = FooRouter(self.connection)

    def test_handle(self):
        data = {'verb': 'call_foo'}
        self.router.handle(data)
        self.assertTrue(self.router.router_called)

    def test_invalid_verb(self):
        data = {'verb': 'invalid_verb'}
        with self.assertRaises(UnexpectedVerbException):
            self.router.handle(data)

    def test_page_context(self):
        data = {'verb': 'call_foo', 'args': {'_page': 12}}
        self.router.handle(data)
        self.assertIn('page', self.router.context)

    def test_permission_fail(self):
        FooRouter.permission_classes = (Permission(), )
        data = {'verb': 'call_foo', 'args': {'permission_pass': False}}
        self.router.handle(data)
        self.assertFalse(self.router.router_called)

    def test_permission_pass(self):
        FooRouter.permission_classes = (Permission(), )
        data = {'verb': 'call_foo', 'args': {'permission_pass': True}}
        self.router.handle(data)
        self.assertTrue(self.router.router_called)
