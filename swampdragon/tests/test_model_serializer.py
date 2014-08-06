from .serializers import FooSerializer, BarSerializer, BazSerializer, QuxSerializer, StaffSerializer, DocumentSerializer
from .models import FooModel, BarModel, BazModel, QuxModel, Company, Document, Staff
from ..tests.dragon_django_test_case import DragonDjangoTestCase


class DeserializerTest(DragonDjangoTestCase):
    def test_meta(self):
        serializer = FooSerializer()
        self.assertIn('test_field_a', serializer.opts.publish_fields)
        self.assertIn('test_field_a', serializer.opts.update_fields)
        self.assertIn('test_field_b', serializer.opts.update_fields)

    def test_deserialize_simple_model(self):
        """
        Deserialize a simple model with no relationships
        """
        data = {'test_field_a': 'foo', 'test_field_b': 'bar'}
        foo = FooSerializer(data=data).save()
        self.assertEqual('foo', foo.test_field_a)
        self.assertEqual('bar', foo.test_field_b)

    def test_deserialize_with_fk(self):
        """
        Deserialize a model with a foreign key
        """
        data = {
            'number': 12,
            'foo': {'test_field_a': 'foo', 'test_field_b': 'bar'}
        }
        bar = BarSerializer(data).save()
        self.assertEqual(bar.number, 12)
        self.assertEqual(bar.foo.test_field_a, 'foo')

    def test_deserialize_reverse_fks(self):
        """
        Deserialize a model with a list of reverse FKs
        """
        data = {
            'test_field_a': 'foo',
            'test_field_b': 'bar',
            'bars': [
                {'number': 52, },
                {'number': 42, },
            ]
        }
        serializer = FooSerializer(data)
        foo = serializer.save()
        self.assertTrue(foo.bars.exists())

    def test_deserialize_one_to_one(self):
        """
        Deserialize a model with a one to one relationship
        """
        data = {
            'name': 'this is baz',

            'bar': {'number': 25}
        }
        baz = BazSerializer(data).save()
        self.assertEqual(baz.name, 'this is baz')
        self.assertEqual(baz.bar.number, 25)

    def test_deserialize_m2m(self):
        data = {
            'test_field_a': 'foo',
            'test_field_b': 'bar',
            'value': 'test',
            'foos': [{'test_field_a': 'a', 'test_field_b': 'b'}]
        }
        qux = QuxSerializer(data).save()
        self.assertTrue(qux.foos.exists())


class SerializerTest(DragonDjangoTestCase):
    def test_serialize_simple_model(self):
        """
        Serialize a model with no FKs
        """
        foo = FooModel.objects.create(test_field_a='hello', test_field_b='world')
        serializer = FooSerializer(instance=foo)
        data = serializer.serialize()
        for pub_field in serializer.opts.publish_fields:
            self.assertIn(pub_field, data)

    def test_serialize_with_fk(self):
        """
        Serialize a model with a foreign key
        """
        foo = FooModel.objects.create(test_field_a='hello', test_field_b='world')
        bar = BarModel.objects.create(number=123, foo=foo)
        serializer = BarSerializer(instance=bar)
        data = serializer.serialize()
        self.assertEqual(data['foo']['test_field_a'], foo.test_field_a)

    def test_serialize_reverse_fks(self):
        """
        Serialize a model with a reverse foreign key.
        Make sure infinite recursion does not occur
        """
        foo = FooModel.objects.create(test_field_a='hello', test_field_b='world')
        foo.bars.add(BarModel.objects.create(number=123))
        foo.bars.add(BarModel.objects.create(number=333))
        serializer = FooSerializer(instance=foo)
        data = serializer.serialize()

    def test_serialize_one_to_one(self):
        """
        Serialize a model with a one to one relationship
        """
        bar = BarModel.objects.create(number=333)
        baz = BazModel.objects.create(name='bazzy', bar=bar)
        serializer = BazSerializer(instance=baz)
        data = serializer.serialize()
        self.assertEqual(data['bar']['number'], 333)
        self.assertEqual(data['name'], 'bazzy')

    def test_serialize_m2m(self):
        """
        Serialize a model with m2m fields
        """
        qux = QuxModel.objects.create(value='qux')
        qux.foos.add(FooModel.objects.create(test_field_a='a', test_field_b='b'))
        serializer = QuxSerializer(instance=qux)
        data = serializer.serialize()
        self.assertEqual(data['value'], 'qux')
        self.assertEqual(data['foos'][0]['test_field_a'], 'a')


class SerializerExtraDataTest(DragonDjangoTestCase):
    '''
    Test that serializers include mappings for ids and _type values
    '''
    def test_serialize_contains_type(self):
        '''
        Ensure that the serializer includes the '_type' property
        as required by the data mapper
        '''
        foo_ser = FooSerializer(instance=FooModel.objects.create(test_field_a='hello', test_field_b='world'))
        data = foo_ser.serialize()
        self.assertEqual(data['_type'], 'foomodel')

    def test_serialize_contains_list_of_related_ids_reverse_m2m(self):
        '''
        Ensure that the serializer include related objects ids
        on a reverse many 2 many relation
        '''
        staff = Staff.objects.create(name='staffy duck')
        document = Document.objects.create(content='test 123')
        staff.documents.add(document)
        ser = StaffSerializer(instance=staff)
        data = ser.serialize()
        self.assertListEqual([staff.pk], data['documents'][0]['staff_id'])

    def test_serialize_contains_list_of_related_ids_m2m(self):
        '''
        Ensure that the serializer include related objects ids
        on a many 2 many relation
        '''
        staff = Staff.objects.create(name='staffy duck')
        document = Document.objects.create(content='test 123')
        staff.documents.add(document)
        ser = DocumentSerializer(instance=document)
        data = ser.serialize()
        self.assertListEqual([document.pk], data['staff_id'])

    def test_serialize_contains_list_of_related_ids_related(self):
        '''
        Ensure that the serializer include related objects ids
        on a many 2 many relation
        '''
        foo = FooModel.objects.create(test_field_a='hello', test_field_b='world', pk=100)
        bar = BarModel.objects.create(number=123, foo=foo)
        ser = BarSerializer(instance=bar)
        data = ser.serialize()
        self.assertListEqual([foo.pk], data['foo_id'])
