from .dragon_test_case import DragonTestCase
from ..route_handler import BaseRouter, LOGIN_REQUIRED, SUCCESS, ERROR
from ..permissions import login_required, LoginRequired, RoutePermission


class TestRouterDecorated(BaseRouter):
    """
    A router with a function decorated
    """
    valid_verbs = ['do_something']

    @login_required
    def do_something(self, **kwargs):
        self.send('all good')


class TestRouter(BaseRouter):
    """
    A router with all functions requiring login
    """
    valid_verbs = ['do_something']
    permission_classes = [LoginRequired()]

    def do_something(self, **kwargs):
        self.send('all good')


class TestRouterSpecific(BaseRouter):
    """
    A router where only one verb requires a signed in user
    """
    valid_verbs = ['free_for_all', 'need_login']
    permission_classes = [LoginRequired(verbs=['need_login'])]

    def free_for_all(self, **kwargs):
        self.send('all good')

    def need_login(self, **kwargs):
        self.send('all good')


class CustomPermission(RoutePermission):
    """
    A custom permission requiring 'ok' to be sent to the handler
    """
    def test_permission(self, handler, verb, **kwargs):
        if 'ok' not in kwargs:
            return self.permission_failed(handler)
        return True

    def permission_failed(self, handler):
        handler.send_error({'ok': ['ok missing']})
        return False


class CustomPermissionRouter(BaseRouter):
    """
    A router with a custom permission
    """
    valid_verbs = ['permission_required']
    permission_classes = [CustomPermission()]

    def permission_required(self, **kwargs):
        self.send('everything is okay')


class BrokenPermission(RoutePermission):
    """
    This permission is missing both required functions of a permission
    *  test_permission
    *  permission_failed
    """
    pass


class BrokenPermissionRouter(BaseRouter):
    valid_verbs = ['do_something']
    permission_classes = [BrokenPermission()]

    def do_something(self, **kwargs):
        pass


class HalfAPermission(RoutePermission):
    def test_permission(self, handler, verb, **kwargs):
        return self.permission_failed(handler)


class HalfAPermissionRouter(BaseRouter):
    valid_verbs = ['do_something']
    permission_classes = [HalfAPermission()]

    def do_something(self, **kwargs):
        pass


class TestPermissions(DragonTestCase):
    def test_login_required_decorator(self):
        router = TestRouterDecorated(self.connection)
        router.handle({'verb': 'do_something'})
        self.assertEqual(self.connection.last_message['context']['state'], LOGIN_REQUIRED)

    def test_login_required_decorator_with_user(self):
        self.connection.user = {'user': 'test user'}
        router = TestRouterDecorated(self.connection)
        router.handle({'verb': 'do_something'})
        self.assertEqual(self.connection.last_message['context']['state'], SUCCESS)

    def test_login_required(self):
        router = TestRouter(self.connection)
        router.handle({'verb': 'do_something'})
        self.assertEqual(self.connection.last_message['context']['state'], LOGIN_REQUIRED)

    def test_login_required_on_one_verb(self):
        router = TestRouterSpecific(self.connection)
        router.handle({'verb': 'free_for_all'})
        self.assertEqual(self.connection.last_message['context']['state'], SUCCESS)

        router.handle({'verb': 'need_login'})
        self.assertEqual(self.connection.last_message['context']['state'], LOGIN_REQUIRED)

    def test_fail_custom_permission(self):
        router = CustomPermissionRouter(self.connection)
        router.handle({'verb': 'permission_required'})
        self.assertEqual(self.connection.last_message['context']['state'], ERROR)

    def test_pass_custom_permission(self):
        router = CustomPermissionRouter(self.connection)
        router.handle({'verb': 'permission_required', 'args': {'ok': True}})
        self.assertEqual(self.connection.last_message['context']['state'], SUCCESS)

    def test_broken_permission(self):
        router = BrokenPermissionRouter(self.connection)
        with self.assertRaises(NotImplementedError):
            router.handle({'verb': 'do_something'})

    def test_permission_missing_permission_failed(self):
        router = HalfAPermissionRouter(self.connection)
        with self.assertRaises(NotImplementedError):
            router.handle({'verb': 'do_something'})
