from swampdragon.testing.dragon_testcase import DragonTestCase
from .models import SDModel, ParentModel, ChildModel
from django.db import models
from swampdragon.serializers.model_serializer import ModelSerializer


class FooOne2OneOM(SDModel):
    name = models.CharField(max_length=20)


class BarOne2OneOM(SDModel):
    foo = models.OneToOneField(FooOne2OneOM)
    number = models.IntegerField()


class FooM2MOM(SDModel):
    name = models.CharField(max_length=20)


class BarM2MOM(SDModel):
    foos = models.ManyToManyField(FooM2MOM)
    number = models.IntegerField()


class FooM2MSerializer(ModelSerializer):
    barm2mom_set = 'BarM2MOMSerializer'

    class Meta:
        model = FooM2MOM
        update_fields = ('name', 'barm2mom_set')


class BarM2MOMSerializer(ModelSerializer):
    foos = FooM2MSerializer

    class Meta:
        model = BarM2MOM
        update_fields = ('number', 'foos')


class FooSerializerOM(ModelSerializer):
    barone2oneom = 'BarSerializerOM'

    class Meta:
        model = FooOne2OneOM
        update_fields = ('name', 'barone2oneom')


class BarSerializerOM(ModelSerializer):
    foo = FooSerializerOM

    class Meta:
        model = BarOne2OneOM


class ParentSerializerOM(ModelSerializer):
    childmodel_set = 'ChildSerializerOM'

    class Meta:
        model = ParentModel
        publish_fields = ('text', 'childmodel_set')


class ChildSerializerOM(ModelSerializer):
    parent = ParentSerializerOM

    class Meta:
        model = ChildModel
        publish_fields = ('number', 'parent')


class TestObjectMap(DragonTestCase):
    def test_get_object_map_for_one2one(self):
        om = FooSerializerOM.get_object_map()
        for m in om:
            self.assertFalse(m['is_collection'])
            if m['parent_type'] == 'fooone2oneom':
                self.assertEqual(m['child_type'], 'barone2oneom')
            else:
                self.assertEqual(m['child_type'], 'fooone2oneom')

    def test_get_object_map_for_reverse_one2one(self):
        om = BarSerializerOM.get_object_map()
        for m in om:
            self.assertFalse(m['is_collection'])
            if m['parent_type'] == 'fooone2oneom':
                self.assertEqual(m['child_type'], 'barone2oneom')
            else:
                self.assertEqual(m['child_type'], 'fooone2oneom')

    def test_get_object_map_for_fk(self):
        om = ChildSerializerOM.get_object_map()
        self.assertEqual(len(om), 2)
        for m in om:
            if m['parent_type'] == 'parentmodel':
                self.assertEqual(m['child_type'], 'childmodel')
            else:
                self.assertEqual(m['child_type'], 'parentmodel')

    def test_get_object_map_for_reverse_fk(self):
        om = ParentSerializerOM.get_object_map()
        self.assertEqual(len(om), 2)
        for m in om:
            if m['parent_type'] == 'parentmodel':
                self.assertEqual(m['child_type'], 'childmodel')
            else:
                self.assertEqual(m['child_type'], 'parentmodel')

    def test_get_object_map_form_m2m(self):
        om = FooM2MSerializer.get_object_map()
        self.assertEqual(len(om), 2)
        for m in om:
            if m['parent_type'] == 'foom2mom':
                self.assertEqual(m['child_type'], 'barm2mom')
            else:
                self.assertEqual(m['child_type'], 'foom2mom')
