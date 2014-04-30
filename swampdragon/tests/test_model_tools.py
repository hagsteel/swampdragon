from .dragon_test_case import DragonTestCase
from .models import Company, Department
from ..model_tools import get_property


# class TestChannelUtils(DragonTestCase):
#     def test_get_related_property(self):
#         comp = Company.objects.create(name='test co', comp_num=123)
#         dep_a = Department.objects.create(company=comp, name='dep a')
#         prop = get_property(comp, 'departments__id__in')
#         import ipdb;ipdb.set_trace()