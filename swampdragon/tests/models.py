from django.db import models


class SDModel(models.Model):
    class Meta:
        app_label = 'tests'
        abstract = True


class TextModel(SDModel):
    text = models.CharField(max_length=100)


class TwoFieldModel(SDModel):
    text = models.CharField(max_length=100)
    number = models.IntegerField()
