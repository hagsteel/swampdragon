from datetime import datetime
from django.db import models


class WithFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name


class MultiFileModel(models.Model):
    text = models.CharField(max_length=100)


class File(models.Model):
    multi_file_model = models.ForeignKey(MultiFileModel, related_name='files')
    file = models.ImageField(upload_to='images')
