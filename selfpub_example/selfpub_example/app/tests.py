from .models import Company, Document, Staff, CompanyOwner
from swampdragon.tests.dragon_django_test_case import DragonDjangoTestCase


class SelfPubExampleTest(DragonDjangoTestCase):
    def test_serialize_models(self):
        company = Company.objects.create(name='test co')
        owner = CompanyOwner.objects.create(company=company, name='John Doe')
