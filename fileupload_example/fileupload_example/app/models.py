from datetime import datetime
from django.db import models


class WithFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.ImageField(upload_to='images')
    created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name
