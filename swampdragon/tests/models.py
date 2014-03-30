from django.db import models
from ..serializers.django_model_serializer import DjangoModelSerializer
from ..models import SelfPublishModel
from .mock_provider import MockProvider
from .serializers import CompanySerializer, DepartmentSerializer, StaffSerializer, DocumentSerializer, LogoSerializer


class TestSelfPublishModel(SelfPublishModel):
    publisher_class = MockProvider


class CompanyLogo(TestSelfPublishModel, models.Model):
    url = models.CharField(max_length=100)
    serializer_class = LogoSerializer


class Company(TestSelfPublishModel, models.Model):
    serializer_class = CompanySerializer
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    logo = models.OneToOneField(CompanyLogo, null=True)


class Department(TestSelfPublishModel, models.Model):
    serializer_class = DepartmentSerializer
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, related_name='departments')


class Staff(TestSelfPublishModel, models.Model):
    serializer_class = StaffSerializer
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='staff', null=True)


class Document(TestSelfPublishModel, models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(default='test doc')
    staff = models.ManyToManyField(Staff, related_name='documents')
    serializer_class = DocumentSerializer


class FooWithAbstractSerializer(DjangoModelSerializer):
    model = 'tests.FooWithAbstractBase'
    publish_fields = ['name']
    update_fields = ['name']


class BarWithAbstractSerializer(DjangoModelSerializer):
    model = 'tests.BarWithAbstractBase'
    publish_fields = ['name', 'is_something']
    update_fields = ['name', 'is_something']


class FooAbstract(TestSelfPublishModel, models.Model):
    class Meta:
        abstract = True


class FooWithAbstractBase(FooAbstract):
    serializer_class = FooWithAbstractSerializer
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.name = 'override: {}'.format(self.name)
        super(FooWithAbstractBase, self).save(*args, **kwargs)


class BarWithAbstractBase(FooAbstract):
    name = models.CharField(max_length=100)
    is_something = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.name = 'override: {}'.format(self.name)
        super(BarWithAbstractBase, self).save(*args, **kwargs)


class TestUser(object):
    def __init__(self, username=None, id=None):
        self.username = username
        self.id = id

    def is_anonymous(self):
        return self.id is None
