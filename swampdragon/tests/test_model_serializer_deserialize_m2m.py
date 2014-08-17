from django.db import models
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import SDModel


class Foo(SDModel):
    name = models.CharField(max_length=20)


class Bar(SDModel):
    foos = models.ManyToManyField(Foo)
    number = models.IntegerField()


class FooSerializer(ModelSerializer):
    bar_set = 'BarSerializer'
    class Meta:
        model = Foo
        update_fields = ('name', 'bar_set')


class BarSerializer(ModelSerializer):
    foos = FooSerializer

    class Meta:
        model = Bar
        update_fields = ('number', 'foos')


class TestModelSerializer(DragonTestCase):
    def test_deserialize_m2m(self):
        data = {
            'number': 3,
            'foos': [
                {'name': 'foo'}
            ]
        }
        serializer = BarSerializer(data)
        bar = serializer.save()
        self.assertEqual(bar.number, data['number'])
        self.assertEqual(bar.foos.first().name, data['foos'][0]['name'])

    def test_deserialize_reverse_m2m(self):
        data = {
            'name': 'foo',
            'bar_set': [
                {'number': 3}
            ]
        }
        serializer = FooSerializer(data)
        foo = serializer.save()
        self.assertEqual(foo.name, data['name'])
        self.assertEqual(foo.bar_set.first().number, data['bar_set'][0]['number'])
