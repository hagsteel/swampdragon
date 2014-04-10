from datetime import datetime
from django.db import models


class WithFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.ImageField(upload_to='temp')
    created = models.DateTimeField(default=datetime.now)
    a_bool = models.BooleanField()

    def __str__(self):
        return self.name
