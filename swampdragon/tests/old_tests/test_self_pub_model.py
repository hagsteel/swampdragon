from .. import route_handler
from ..route_handler import BaseModelPublisherRouter
from .models import Company, CompanySerializer, FooWithAbstractBase, FooWithAbstractSerializer, BarWithAbstractBase, \
    BarWithAbstractSerializer, Department, Staff, Document
from .mock_connection import TestConnection
from .serializers import DocumentSerializer, DepartmentSerializer, StaffSerializer
from .dragon_django_test_case import DragonDjangoTestCase


class DocumentRouter(BaseModelPublisherRouter):
    model = Document
    route_name = 'test_doc_router'
    serializer_class = DocumentSerializer

    def get_query_set(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def get_object(self, **kwargs):
        return self.model.objects.get(**kwargs)


class CompanyRouter(BaseModelPublisherRouter):
    model = Company
    route_name = 'test_company_router'
    serializer_class = CompanySerializer
    include_related = [DepartmentSerializer]

    def get_query_set(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def get_object(self, **kwargs):
        return self.model.objects.get(**kwargs)


class FooWithAbstractRouter(BaseModelPublisherRouter):
    model = FooWithAbstractBase
    route_name = 'test_foo_abs_router'
    serializer_class = FooWithAbstractSerializer

    def get_query_set(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def get_object(self, **kwargs):
        return self.model.objects.get(**kwargs)


class BarWithAbstractRouter(BaseModelPublisherRouter):
    model = BarWithAbstractBase
    route_name = 'test_foo_abs_router'
    serializer_class = BarWithAbstractSerializer

    def get_query_set(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def get_object(self, **kwargs):
        return self.model.objects.get(**kwargs)


class TestSelfPubModel(DragonDjangoTestCase):
    def setUp(self):
        route_handler.register(CompanyRouter)
        route_handler.register(FooWithAbstractRouter)
        route_handler.register(DocumentRouter)
        self.connection = TestConnection()
        self.company_handler = route_handler.get_route_handler(CompanyRouter.route_name)
        self.foo_abs_handler = route_handler.get_route_handler(FooWithAbstractRouter.route_name)
        self.bar_abs_handler = route_handler.get_route_handler(BarWithAbstractRouter.route_name)
        self.document_handler = route_handler.get_route_handler(DocumentRouter.route_name)

    def test_self_publish(self):
        kwargs = {'channel': 'client_chan', }
        self.company_handler(self.connection).subscribe(**kwargs)
        foo = Company.objects.create(name='foo', comp_num=33)
        json_data = self.connection.get_last_published_data()
        serialized_foo = foo.serialize()
        self.assertDictEqual(serialized_foo, json_data)

    def test_self_publish_with_abstract(self):
        kwargs = {'channel': 'client_chan', }
        self.foo_abs_handler(self.connection).subscribe(**kwargs)
        foo = FooWithAbstractBase.objects.create(name='foo')
        json_data = self.connection.get_last_published_data()
        serialized_foo = foo.serialize()
        self.assertDictEqual(serialized_foo, json_data)

    def test_self_publish_with_abstract_without_serializer(self):
        '''
        Assure it raises an exception, as the BarWithAbstractBase does not have
        a serializer class
        '''
        kwargs = {'channel': 'client_chan', }
        self.bar_abs_handler(self.connection).subscribe(**kwargs)
        with self.assertRaises(TypeError):
            BarWithAbstractBase.objects.create(name='foo')

    def test_only_publish_changes(self):
        kwargs = {'channel': 'client_chan', }
        self.company_handler(self.connection).subscribe(**kwargs)
        foo = Company.objects.create(name='foo', comp_num=33)

        self.connection.sent_data = []
        foo.comp_num = 33
        foo.save()
        self.assertEqual(len(self.connection.sent_data), 0)

        foo.comp_num = 34
        foo.save()
        data = self.connection.get_last_published_data()
        self.assertEqual(data['comp_num'], foo.comp_num)

    def test_publish_based_on_children(self):
        with Company(name='foo company', comp_num=33) as company:
            pass
        with Department(name='department a', company=company) as department:
            pass
        self.connection.subscribe('test_company_router', 'cli_chan', {'name__contains': 'foo'})

        department.name = 'updated'
        department.save()
        self.assertGreater(len(self.connection.published_data), 0)

    def test_no_publish_based_on_childrens_children(self):
        kwargs = {'channel': 'client_chan', 'id': 1}
        company = Company.objects.create(name='company a', comp_num=33)
        department = Department.objects.create(name='department a', company=company)
        Staff.objects.create(name='John', department=department)
        dont_publish_staff = Staff.objects.create(
            name='no pub staff',
            department=Department.objects.create(name='foo', company=Company.objects.create(name='foo2', comp_num=33)),
        )
        self.company_handler(self.connection).subscribe(**kwargs)
        self.connection.sent_data = []
        dont_publish_staff.name = 'updated'
        dont_publish_staff.save()
        self.assertEqual(len(self.connection.sent_data), 0)

    def test_get_changes(self):
        kwargs = {'channel': 'client_chan', }
        self.company_handler(self.connection).subscribe(**kwargs)
        foo = Company.objects.create(name='foo', comp_num=33)
        expected = foo._get_changes()
        foo.comp_num = 33
        actual = foo._get_changes()
        self.assertDictEqual(expected, actual)

    def test_m2m(self):
        kwargs = {'channel': 'client_chan'}
        self.document_handler(self.connection).subscribe(**kwargs)
        with Staff(name='John') as staff_a:
            pass
        with Staff(name='Tina') as staff_b:
            pass

        self.connection.sent_data = []

        with Document(name='test doc') as document:
            document.save()
            document.staff.add(staff_a)
            document.staff.add(staff_b)
        document.name = 'test doc updated'
        document.save()
        self.assertEqual(len(self.connection.published_data), 3)

    def test_remove_on_update(self):
        with Company(name='foo', comp_num=55) as company:
            pass
        kwargs = {'channel': 'client_chan', 'name': 'foo'}
        self.company_handler(self.connection).subscribe(**kwargs)
        company.name = 'updated'
        company.save()
        last_update = self.connection.get_last_published()
        self.assertEqual(last_update['action'], 'deleted')
