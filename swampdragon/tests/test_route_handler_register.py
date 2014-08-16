from ..route_handler import BaseRouter, BaseModelRouter
from .. import route_handler
from .dragon_test_case import DragonTestCase


class Router(BaseRouter):
    route_name = 'test-router'


class ModelRouterGetObject(BaseModelRouter):
    route_name = 'model-router'

    def get_object(self, **kwargs):
        pass


class ModelRouterGetQuerySet(BaseModelRouter):
    route_name = 'model-router'

    def get_query_set(self, **kwargs):
        pass


class TestRouteHandler(DragonTestCase):
    def test_register_router(self):
        route_handler.register(Router)
        self.assertIsNotNone(route_handler.get_route_handler(Router.get_name()))

    def test_register_router_twice(self):
        route_handler.register(Router)
        route_handler.register(Router)
        self.assertEqual(len(route_handler.registered_handlers), 1)

    def test_register_model_router_with_missing_get_object(self):
        with self.assertRaises(Exception):
            route_handler.register(ModelRouterGetObject)

    def test_register_model_router_with_missing_get_query_set(self):
        with self.assertRaises(Exception):
            route_handler.register(ModelRouterGetQuerySet)
