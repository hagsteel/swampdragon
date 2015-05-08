from datetime import datetime
from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter
from swampdragon.testing.dragon_testcase import DragonTestCase
from .models import BarSelfPub, FooSelfPub
from .serializers import BarSelfPubSerializer


class BarRouter(ModelRouter):
    valid_verbs = ['subscribe']
    route_name = 'bar-router'
    model = BarSelfPub
    serializer_class = BarSelfPubSerializer


class TestRelatedModelChange(DragonTestCase):
    def setUp(self):
        super(TestRelatedModelChange, self).setUp()
        route_handler.register(BarRouter)

    def test_alter_related_model(self):
        """
        Changing a self publishing
        """
        foo = FooSelfPub.objects.create(name='test', number=123)
        new_foo = FooSelfPub.objects.create(name='test two', number=456)
        bar = BarSelfPub.objects.create(date=datetime.now(), foo=foo)

        self.connection.subscribe(BarRouter.route_name, 'test')

        self.assertIsNone(self.connection.last_pub)
        bar.foo = new_foo
        bar.save()
        self.assertIsNotNone(self.connection.last_pub)
