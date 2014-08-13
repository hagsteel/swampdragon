import json
from .. import route_handler
from ..route_handler import BaseRouter
from ..permissions import login_required, LoginRequired
from .mock_connection import TestConnection
from .models import TestUser
from .dragon_django_test_case import DragonDjangoTestCase


class PermissionRouter(BaseRouter):
    route_name = 'test_permission_attr_router'
    valid_verbs = ['test_perm']

    @login_required
    def test_perm(self, **kwargs):
        self.send('foo')


class PermissionClassRouter(BaseRouter):
    route_name = 'test_permission_class_router'
    valid_verbs = ['test_perm']
    permission_classes = [LoginRequired()]

    def test_perm(self, **kwargs):
        self.send('foo')


class TestPermissions(DragonDjangoTestCase):
    def setUp(self):
        route_handler.register(PermissionRouter)
        self.permission_handler = route_handler.get_route_handler(PermissionRouter.route_name)

    def test_permission_decorator_anonymous_user(self):
        data = {'verb': 'test_perm'}
        connection = TestConnection()
        self.permission_handler(connection).handle(data)
        json_data = json.loads(connection.sent_data[-1])
        self.assertEqual(json_data['context']['state'], 'login_required')
        self.assertNotEqual(json_data['data'], 'foo')

    def test_permission_decorator_user(self):
        data = {'verb': 'test_perm'}
        connection = TestConnection(user=TestUser(username='testuser', id=1))
        self.permission_handler(connection).handle(data)
        json_data = json.loads(connection.sent_data[-1])
        self.assertEqual(json_data['context']['state'], 'success')
        self.assertEqual(json_data['data'], 'foo')


class TestClassPermissions(DragonDjangoTestCase):
    def setUp(self):
        route_handler.register(PermissionClassRouter)
        self.permission_handler = route_handler.get_route_handler(PermissionClassRouter.route_name)

    def test_permission_dectorator_anonymous_user(self):
        data = {'verb': 'test_perm'}
        connection = TestConnection()
        self.permission_handler(connection).handle(data)
        json_data = json.loads(connection.sent_data[-1])
        self.assertEqual(json_data['context']['state'], 'login_required')
        self.assertNotEqual(json_data['data'], 'foo')

    def test_permission_dectorator_user(self):
        data = {'verb': 'test_perm'}
        connection = TestConnection(user=TestUser(username='testuser', id=1))
        self.permission_handler(connection).handle(data)
        json_data = json.loads(connection.sent_data[-1])
        self.assertEqual(json_data['context']['state'], 'success')
        self.assertEqual(json_data['data'], 'foo')
