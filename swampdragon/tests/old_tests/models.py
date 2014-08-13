from django.db import models
from ..models import SelfPublishModel
from .mock_provider import MockPubSubProvider
from .serializers import CompanySerializer, DepartmentSerializer, StaffSerializer, DocumentSerializer, LogoSerializer, \
    FooSerializer, BarSerializer, CacheFooSerializer, CacheBarSerializer
from ..serializers.model_serializer import ModelSerializer


class TestSelfPublishModel(SelfPublishModel):
    publisher_class = MockPubSubProvider


class CompanyLogo(TestSelfPublishModel, models.Model):
    url = models.CharField(max_length=100)
    serializer_class = LogoSerializer


class Company(TestSelfPublishModel, models.Model):
    serializer_class = CompanySerializer
    name = models.CharField(max_length=100)
    comp_num = models.PositiveIntegerField()
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


class FooWithAbstractSerializer(ModelSerializer):
    class Meta:
        model = 'tests.FooWithAbstractBase'
        publish_fields = ['name']
        update_fields = ['name']


class BarWithAbstractSerializer(ModelSerializer):
    class Meta:
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


class FooModel(TestSelfPublishModel, models.Model):
    serializer_class = FooSerializer
    test_field_a = models.CharField(max_length=100)
    test_field_b = models.CharField(max_length=100)


class BarModel(TestSelfPublishModel, models.Model):
    serializer_class = BarSerializer
    number = models.IntegerField()
    foo = models.ForeignKey(FooModel, related_name='bars', null=True, blank=True)


class BazModel(models.Model):
    name = models.CharField(max_length=100)
    bar = models.OneToOneField(BarModel, null=True, blank=True)


class QuxModel(models.Model):
    value = models.CharField(max_length=100)
    foos = models.ManyToManyField(FooModel)


class CacheFooModel(TestSelfPublishModel, models.Model):
    serializer_class = CacheFooSerializer
    test_field_a = models.CharField(max_length=100)
    test_field_b = models.CharField(max_length=100)


class CacheBarModel(TestSelfPublishModel, models.Model):
    serializer_class = CacheBarSerializer
    number = models.IntegerField()
    foo = models.ForeignKey(CacheFooModel, related_name='bars', null=True)
