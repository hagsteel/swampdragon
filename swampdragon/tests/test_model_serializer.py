from .serializers import FooSerializer, BarSerializer, BazSerializer
from ..tests.dragon_django_test_case import DragonDjangoTestCase


class SerializerTest(DragonDjangoTestCase):
    def test_meta(self):
        serializer = FooSerializer()
        self.assertIn('test_field_a', serializer.opts.publish_fields)
        self.assertIn('test_field_a', serializer.opts.update_fields)
        self.assertIn('test_field_b', serializer.opts.update_fields)

    def test_serialize_simple_model(self):
        data = {'test_field_a': 'foo', 'test_field_b': 'bar'}
        foo = FooSerializer(data=data).save()
        self.assertEqual('foo', foo.test_field_a)
        self.assertEqual('bar', foo.test_field_b)

    def test_serialize_with_fk(self):
        # data = {'name': 'smint'}
        # baz = BazSerializer(data).save()

        data = {
            'number': 12,
            'foo': {'test_field_a': 'foo', 'test_field_b': 'bar'}
        }
        bar = BarSerializer(data).save()
        self.assertEqual(bar.number, 12)
        self.assertEqual(bar.foo.test_field_a, 'foo')

    def test_serialize_reverse_fk(self):
        data = {
            'test_field_a': 'foo',
            'test_field_b': 'bar',
            'bars': [
                {'number': 52,},
                {'number': 42,},
            ]
        }
        serializer = FooSerializer(data)
        foo = serializer.save()
        self.assertTrue(foo.bars.exists())

    def test_serialize_one_to_one(self):
        data = {
            'name': 'this is baz',
            'bar': {'number': 25}
        }

        baz = BazSerializer(data).save()
        self.assertEqual(baz.name, 'this is baz')
        self.assertEqual(baz.bar.number, 25)

    def test_serialize_nested_fk(self):
        data = {
            'name': 'this is baz',
            'bar': {'number': 25}
        }
