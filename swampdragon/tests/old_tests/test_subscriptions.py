from .dragon_django_test_case import DragonDjangoTestCase
from swampdragon import route_handler
from .models import FooModel, BarModel
from .test_route_handler import FooRouter


class SubscriptionTest(DragonDjangoTestCase):
    def setUp(self):
        route_handler.register(FooRouter)

    def test_subscribe_to_related_via_router(self):
        foo = FooModel.objects.create(test_field_a='foo a', test_field_b='foo b')
        bar = BarModel.objects.create(foo=foo, number=1)
        self.connection.subscribe(FooRouter.route_name, 'cli-chan', {'bars__number_gte': 10})
        bar.number = 110
        bar.save()
        # import ipdb;ipdb.set_trace()
