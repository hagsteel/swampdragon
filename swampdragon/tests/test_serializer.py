from datetime import datetime
from decimal import Decimal
from django_webtest import WebTest
from ..serializers.base_serializer import BaseSerializer
from ..serializers.serializer_importer import get_serializer, _imported_modules_
from .models import CompanySerializer, Company, Department, Staff, Document
from .mock_connection import TestConnection
from .serializers import DocumentSerializer, DepartmentSerializer, StaffSerializer


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


class SerializerTest(WebTest):
    def setUp(self):
        self.connection = TestConnection()

    def test_custom_serializer(self):
        to = TestObjectWithSerializer('foo', 12)
        data = TestObjectSerializer().serialize(to)
        self.assertEqual('foo', data['name'])
        self.assertEqual(12, data['numval'])
        self.assertTrue(isinstance(data['created'], str))
        self.assertTrue(isinstance(data['dec_value'], str))

    def test_get_object_map(self):
        company_graph = CompanySerializer().get_object_map()
        self.assertEqual(len(company_graph), 2)
        company_graph = CompanySerializer().get_object_map([StaffSerializer])
        self.assertEqual(len(company_graph), 3)
        department_graph = DepartmentSerializer.get_object_map()
        self.assertEqual(len(department_graph), 1)
        staff_graph = StaffSerializer.get_object_map()
        self.assertEqual(len(staff_graph), 1)
        self.assertEqual(staff_graph[0]['via'], 'staff_id')

    def test_m2m_serialization(self):
        with Company() as company:
            company.name = 'company a'
            company.age = 33

        with Department() as department:
            department.name = 'dep a'
            department.company = company

        with Document() as document:
            document.name = 'test doc'
            document.pk = 100

        with Staff() as staff:
            staff.name = 'John Doe'
            staff.department = department
            staff.pk = 123

        staff.documents.add(document)
        doc_ser = DocumentSerializer(document).serialize()
        self.assertIn(staff.pk, doc_ser['staff_id'])
        self.assertIn(document.pk, doc_ser['staff'][0]['document_id'])

    def test_get_serializer_from_string(self):
        ser = get_serializer('tests.DocumentSerializer', self.__class__)
        self.assertEqual(ser, DocumentSerializer)
        self.assertNotEqual(_imported_modules_, {})
