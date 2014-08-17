from django.db import models
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import TextModel, SDModel


class FooOne2One(SDModel):
    name = models.CharField(max_length=20)


class BarOne2One(SDModel):
    foo = models.OneToOneField(FooOne2One)
    number = models.IntegerField()


class FooSerializer(ModelSerializer):
    bar = 'BarSerializer'

    class Meta:
        model = FooOne2One
        update_fields = ('name', 'bar')


class BarSerializer(ModelSerializer):
    foo = FooSerializer

    class Meta:
        model = BarOne2One
        update_fields = ('number', 'foo')


class TestModelSerializer(DragonTestCase):
    def test_deserialize_with_one_2_one(self):
        data = {
            'name': 'foo',
            'bar': {'number': 5}
        }
        serializer = FooSerializer(data)
        foo = serializer.save()
        self.assertEqual(foo.name, data['name'])
        self.assertEqual(foo.bar.number, data['bar']['number'])

    def test_deserialize_with_reverse_one_2_one(self):
        data = {
            'number': 123,
            'foo': {'name': 'foo'}
        }
        serializer = BarSerializer(data)
        bar = serializer.save()
        self.assertEqual(bar.number, data['number'])
        self.assertEqual(bar.foo.name, data['foo']['name'])
