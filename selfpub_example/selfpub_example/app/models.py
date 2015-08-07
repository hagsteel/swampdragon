from django.db import models
from swampdragon.models import SelfPublishModel
from .serializers import CompanySerializer, StaffSerializer, DocumentSerializer, CompanyOwnerSerializer


class Company(SelfPublishModel, models.Model):
    name = models.CharField(max_length=100)
    serializer_class = CompanySerializer

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = "companies"


class CompanyOwner(SelfPublishModel, models.Model):
    name = models.CharField(max_length=100)
    company = models.OneToOneField(Company)
    serializer_class = CompanyOwnerSerializer

    def __str__(self):
        return self.name


class Staff(SelfPublishModel, models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, related_name='staff')
    serializer_class = StaffSerializer

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = "staff"


class Document(SelfPublishModel, models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    staff = models.ManyToManyField(Staff, related_name='documents', null=True, blank=True)
    serializer_class = DocumentSerializer

    def __str__(self):
        return self.title
