from swampdragon.models import SelfPublishModel
from django.db import models
from .serializers import FooSelfPubSerializer, BarSelfPubSerializer, BoolSelfPubSerializer


class SDModel(models.Model):
    class Meta:
        app_label = 'tests'
        abstract = True


class TextModel(SDModel):
    text = models.CharField(max_length=100)


class TwoFieldModel(SDModel):
    text = models.CharField(max_length=50)
    number = models.IntegerField()


class ParentModel(SDModel):
    name = models.CharField(max_length=100)


class ChildModel(SDModel):
    parent = models.ForeignKey(ParentModel)
    number = models.IntegerField()


class FooSelfPub(SelfPublishModel, SDModel):
    serializer_class = FooSelfPubSerializer
    name = models.CharField(max_length=100)
    number = models.IntegerField(null=True)


class BarSelfPub(SelfPublishModel, SDModel):
    serializer_class = BarSelfPubSerializer
    date = models.DateTimeField()
    foo = models.ForeignKey(FooSelfPub, related_name='bars')


class BoolSelfPub(SelfPublishModel, SDModel):
    serializer_class = BoolSelfPubSerializer
    bool = models.BooleanField(default=False)
