from .dragon_django_test_case import DragonDjangoTestCase
from .serializers import FooSerializer, BarSerializer, BazSerializer, QuxSerializer, CompanySerializer, DepartmentSerializer, StaffSerializer
from .models import Company, CompanyLogo, Department, Staff


class ObjectMapTest(DragonDjangoTestCase):
    def test_get_object_map(self):
        foo_graph = FooSerializer.get_object_map()
        bar_graph = BarSerializer.get_object_map()
        baz_graph = BazSerializer.get_object_map()
        qux_graph = QuxSerializer.get_object_map()

        company_graph = CompanySerializer.get_object_map()
        dep_graph = DepartmentSerializer.get_object_map()
        staff_graph = StaffSerializer.get_object_map()

        company = Company.objects.create(name='test co', comp_num=1)
        dep = Department.objects.create(company=company)
