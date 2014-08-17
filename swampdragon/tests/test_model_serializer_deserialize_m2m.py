from django.db import models
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import SDModel


class FooM2M(SDModel):
    name = models.CharField(max_length=20)


class BarM2M(SDModel):
    foos = models.ManyToManyField(FooM2M)
    number = models.IntegerField()


class FooM2MSerializer(ModelSerializer):
    barm2m_set = 'BarM2MSerializer'
    class Meta:
        model = FooM2M
        update_fields = ('name', 'barm2m_set')


class BarM2MSerializer(ModelSerializer):
    foos = FooM2MSerializer

    class Meta:
        model = BarM2M
        update_fields = ('number', 'foos')


class TestModelSerializer(DragonTestCase):
    def test_deserialize_m2m(self):
        data = {
            'number': 3,
            'foos': [
                {'name': 'foo'}
            ]
        }
        serializer = BarM2MSerializer(data)
        bar = serializer.save()
        self.assertEqual(bar.number, data['number'])
        self.assertEqual(bar.foos.first().name, data['foos'][0]['name'])

    def test_deserialize_reverse_m2m(self):
        data = {
            'name': 'foo',
            'barm2m_set': [
                {'number': 3}
            ]
        }
        serializer = FooM2MSerializer(data)
        foo = serializer.save()
        self.assertEqual(foo.name, data['name'])
        self.assertEqual(foo.barm2m_set.first().number, data['barm2m_set'][0]['number'])
