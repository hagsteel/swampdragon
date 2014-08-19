from .models import Company, Document, Staff, CompanyOwner
from .serializers import StaffSerializer
from swampdragon.tests.dragon_test_case import DragonTestCase


class SelfPubExampleTest(DragonTestCase):
    def test_serialize_models(self):
        companya = Company.objects.create(name='test co')
        companyb = Company.objects.create(name='test co')
        owner = CompanyOwner.objects.create(company=companya, name='John Doe')
        staff = Staff.objects.create(company=companya, name='John Smith')
