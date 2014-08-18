from datetime import datetime
from ..route_handler import ModelRouter
from .dragon_test_case import DragonTestCase
from .models import FooSelfPub, BarSelfPub
from .serializers import FooSelfPubSerializer, BarSelfPubSerializer


class FooModelRouter(ModelRouter):
    serializer_class = FooSelfPubSerializer


class BarModelRouter(ModelRouter):
    serializer_class = BarSelfPubSerializer


class TestSelfPubModel(DragonTestCase):
    def test_self_pub_model(self):
        router = FooModelRouter(self.connection)
        router.subscribe(**{'channel': 'testchan'})
        self.assertIsNone(self.connection.last_pub)
        FooSelfPub.objects.create(name='test')
        self.assertIsNotNone(self.connection.last_pub)

    def test_self_pub_model_with_fk(self):
        router = BarModelRouter(self.connection)
        router.subscribe(**{'channel': 'testchan'})
        self.assertIsNone(self.connection.last_pub)
        foo = FooSelfPub.objects.create(name='test')
        BarSelfPub.objects.create(date=datetime.now(), foo=foo)
        self.assertIsNotNone(self.connection.last_pub)

    def test_ignore_id_when_getting_updated_fields(self):
        FooSelfPubSerializer.Meta.publish_fields += ('pk', )
        foo = FooSelfPub.objects.create(name='test')

    def test_get_changes(self):
        foo = FooSelfPub.objects.create(name='test')
        self.assertDictEqual(foo.get_changes(), {})
        foo.number = 12
        self.assertDictEqual(foo.get_changes(), {'number': 12})
        foo.number = 55
        self.assertDictEqual(foo.get_changes(), {'number': 55})
        foo.name = 'updated'
        self.assertDictEqual(foo.get_changes(), {'name': 'updated', 'number': 55})
        foo.name = 'foo'
        foo.number = 1
        self.assertDictEqual(foo.get_changes(), {'name': 'foo', 'number': 1})

        bar = BarSelfPub.objects.create(date=datetime.now(), foo=foo)
        self.assertDictEqual(bar.get_changes(), {})
        update_date = datetime.now()
        bar.date = update_date
        self.assertDictEqual(bar.get_changes(), {'date': update_date})

    def test_raise_validation_error(self):
        foo = FooSelfPub.objects.create(name='test')
        data = foo.serialize()
        self.assertEqual(data['name'], foo.name)

    def test_create(self):
        router = FooModelRouter(self.connection)
        router.subscribe(**{'channel': 'testchan'})
        FooSelfPub.objects.create(name='test')
        self.assertEqual(self.connection.last_pub['action'], 'created')

    def test_update(self):
        router = FooModelRouter(self.connection)
        router.subscribe(**{'channel': 'testchan'})
        foo = FooSelfPub.objects.create(name='test')
        foo.name = 'updated'
        foo.save()
        self.assertEqual(self.connection.last_pub['action'], 'updated')
