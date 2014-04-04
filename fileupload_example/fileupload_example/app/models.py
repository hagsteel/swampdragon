from django.db import models


class WithFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.ImageField(upload_to='temp')
