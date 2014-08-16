from ..route_handler import BaseRouter
from .dragon_test_case import DragonTestCase


class FooRouter(BaseRouter):
    route_name = 'foo'


class NamelessRrouter(BaseRouter):
    pass


class TestBaseRouter(DragonTestCase):
    def test_get_name(self):
        self.assertEqual(FooRouter.get_name(), FooRouter.route_name)

    def test_name_missing(self):
        with self.assertRaises(Exception):
            NamelessRrouter.get_name()
