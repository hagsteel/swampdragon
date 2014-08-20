from datetime import datetime
from ..route_handler import ModelRouter
from ..pubsub_providers.base_provider import PUBACTIONS
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
        self.assertListEqual(foo.get_changed_fields(), [])
        foo.number = 12
        self.assertListEqual(foo.get_changed_fields(), ['number'])
        foo.name = 'updated'
        self.assertIn('number', foo.get_changed_fields())
        self.assertIn('name', foo.get_changed_fields())

        bar = BarSelfPub.objects.create(date=datetime.now(), foo=foo)
        self.assertListEqual(bar.get_changed_fields(), [])
        update_date = datetime.now()
        bar.date = update_date
        self.assertListEqual(bar.get_changed_fields(), ['date'])

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

    def test_remove_on_update(self):
        router = FooModelRouter(self.connection)
        router.subscribe(**{'channel': 'testchan', 'name__contains': 'findme'})
        foo = FooSelfPub.objects.create(name='test')
        self.assertIsNone(self.connection.last_pub)
        foo.name = 'findme'
        foo.save()
        self.assertEqual(self.connection.last_pub['action'], PUBACTIONS.updated)

        foo.name = 'hideme'
        foo.save()
        self.assertEqual(self.connection.last_pub['action'], PUBACTIONS.deleted)

        foo.name = 'findmeagain'
        foo.save()
        self.assertEqual(self.connection.last_pub['action'], PUBACTIONS.updated)
