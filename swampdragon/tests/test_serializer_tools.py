from django.db import models
from .dragon_test_case import DragonTestCase
from swampdragon.tests.models import SDModel


class ReverseM2M(SDModel):
    number = models.IntegerField()


class M2M(SDModel):
    name = models.CharField(max_length=10)
    many = models.ManyToManyField(ReverseM2M)



class TestSerializerTools(DragonTestCase):
    def test_m2m(self):
        pass

    def test_reverse_m2m(self):
        pass

    def test_fk(self):
        pass

    def test_reverse_fk(self):
        pass

    def test_one2one(self):
        pass

    def test_reverse_one2one(self):
        pass
