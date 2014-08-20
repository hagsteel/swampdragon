from .models import Company, Document, Staff, CompanyOwner
from .serializers import StaffSerializer, CompanySerializer
from swampdragon.serializers import serializer_tools
from swampdragon.tests.dragon_test_case import DragonTestCase


class SelfPubExampleTest(DragonTestCase):
    def test_serialize_models(self):
        companya = Company.objects.create(name='test co')
        # companyb = Company.objects.create(name='test co')
        # owner = CompanyOwner.objects.create(company=companya, name='John Doe')
        staff = Staff.objects.create(company=companya, name='John Smith')
        doc = Document.objects.create(title='random title', content='abc 123')
        # ser = CompanySerializer(instance=companya)
        # data = ser.serialize()

        import ipdb;ipdb.set_trace()
        # ser = StaffSerializer(instance=staff)
        # data = ser.serialize()