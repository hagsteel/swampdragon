from datetime import datetime
from decimal import Decimal
from ..serializers.base_serializer import BaseSerializer
from ..serializers.serializer_importer import get_serializer, _imported_modules_
from .models import Company, Department, Staff, Document, FooModel, BarModel
from .mock_connection import TestConnection
from .serializers import DocumentSerializer, FooSerializer
from .dragon_django_test_case import DragonDjangoTestCase


class TestObject(object):
    def __init__(self, name, numval):
        super(TestObject, self).__init__()
        self.name = name
        self.numval = numval
        self.created = datetime.now()


class TestObjectSerializer(BaseSerializer):
    publish_fields = ['name', 'numval', 'created', 'dec_value']


class TestObjectWithSerializer(object):
    def __init__(self, name, numval):
        super(TestObjectWithSerializer, self).__init__()
        self.name = name
        self.numval = numval
        self.created = datetime.now()
        self.dec_value = Decimal(12.44)


class SerializerTest(DragonDjangoTestCase):
    def setUp(self):
        self.connection = TestConnection()

    def test_custom_serializer(self):
        to = TestObjectWithSerializer('foo', 12)
        data = TestObjectSerializer().serialize(to)
        self.assertEqual('foo', data['name'])
        self.assertEqual(12, data['numval'])
        self.assertTrue(isinstance(data['created'], str))
        self.assertTrue(isinstance(data['dec_value'], str))

    def test_m2m_serialization(self):
        with Company() as company:
            company.name = 'company a'
            company.comp_num = 33
            company.pk = 321

        with Department() as department:
            department.name = 'dep a'
            department.company = company

        with Document() as document:
            document.name = 'test doc'

        with Staff() as staff:
            staff.name = 'John Doe'
            staff.department = department
            staff.pk = 123

        staff.documents.add(document)
        doc_ser = DocumentSerializer(instance=document).serialize()
        self.assertEqual(staff.pk, doc_ser['staff'][0]['id'])

    def test_get_serializer_from_string(self):
        ser = get_serializer('tests.DocumentSerializer', self.__class__)
        self.assertEqual(ser, DocumentSerializer)
        self.assertNotEqual(_imported_modules_, {})

    def test_serialize_include_via(self):
        '''
        Ensure serializing related models includes the 'via' field
        to help with the object mapper
        '''
        foo = FooModel.objects.create(test_field_a='test')
        bar = BarModel.objects.create(number=123, foo=foo)
        data = FooSerializer(instance=foo).serialize()
        self.assertEqual(data['bars'][0]['foo_id'], foo.pk)
