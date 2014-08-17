from django.db import models
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import TextModel, SDModel


class Parent(SDModel):
    name = models.CharField(max_length=20)


class Child(SDModel):
    parent = models.ForeignKey(Parent)
    number = models.IntegerField()


class ChildSerializer(ModelSerializer):
    parent = 'ParentSerializer'

    class Meta:
        model = Child
        update_fields = ('number', 'parent')


class ParentSerializer(ModelSerializer):
    child_set = ChildSerializer

    class Meta:
        model = Parent
        publish_fields = ('name')
        update_fields = ('name', 'child_set')


class TestModelSerializer(DragonTestCase):
    def test_deserialize_with_fk(self):
        data = {
            'name': 'foo',
            'child_set': [
                {'number': 5}
            ]
        }
        serializer = ParentSerializer(data)
        parent = serializer.save()
        self.assertEqual(parent.name, data['name'])
        self.assertEqual(parent.child_set.first().number, data['child_set'][0]['number'])

    def test_deserialize_with_reverse_fk(self):
        data = {
            'number': 123,
            'parent': {
                'name': 'foo'
            }
        }
        serializer = ChildSerializer(data)
        child = serializer.save()
        self.assertEqual(child.number, data['number'])
        self.assertEqual(child.parent.name, data['parent']['name'])

    def test_get_object_map(self):
        """
        The object map should return information on how to map parents to children
        and vice versa
        """
        object_map = ParentSerializer.get_object_map()
        self.assertLessEqual(len(object_map), 2)
        for om in object_map:
            self.assertIn('via', om)
