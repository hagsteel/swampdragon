from swampdragon.route_handler import BaseRouter
from swampdragon.testing.dragon_testcase import DragonTestCase


class FooRouter(BaseRouter):
    route_name = 'foo'


class TestBaseRouter(DragonTestCase):
    def setUp(self):
        self.router = FooRouter(self.connection)

    def test_get_list(self):
        with self.assertRaises(NotImplementedError):
            self.router.get_list()

    def test_get_single(self):
        with self.assertRaises(NotImplementedError):
            self.router.get_single()

    def test_create(self):
        with self.assertRaises(NotImplementedError):
            self.router.create()

    def test_update(self):
        with self.assertRaises(NotImplementedError):
            self.router.update()

    def test_delete(self):
        with self.assertRaises(NotImplementedError):
            self.router.delete()
