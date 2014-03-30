from django.db import models


class ParentModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()


class ChildModel(models.Model):
    parent = models.ForeignKey(ParentModel, related_name='children')
    name = models.CharField(max_length=100)


class SubChildModel(models.Model):
    child = models.ForeignKey(ChildModel, related_name='subchildren')
    name = models.CharField(max_length=100)
