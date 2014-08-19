from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import ParentModel, ChildModel


class ParentSerializer(ModelSerializer):
    childmodel_set = 'ChildSerializer'

    class Meta:
        model = ParentModel
        publish_fields = ('text', 'childmodel_set')


class ChildSerializer(ModelSerializer):
    parent = ParentSerializer

    class Meta:
        model = ChildModel
        publish_fields = ('number', 'parent')


class ChildModelSerializer(ModelSerializer):
    class Meta:
        model = ChildModel
        publish_fields = ('number', 'parent',)


class ParentModelSerializer(ModelSerializer):
    class Meta:
        model = ParentModel
        publish_fields = ('name', 'childmodel_set')


class TestModelSerializer(DragonTestCase):
    def test_serialize_fk(self):
        parent = ParentModel.objects.create(name='hello world')
        child = ChildModel.objects.create(number=5, parent=parent)
        result = ChildSerializer(instance=child).serialize()
        self.assertIsNotNone(result['parent'])

    def test_reverse_fk(self):
        parent = ParentModel.objects.create(name='hello world')
        child = ChildModel.objects.create(number=5, parent=parent)
        result = ParentSerializer(instance=parent).serialize()
        self.assertIsNotNone(result['childmodel_set'])

    def test_serialize_ignore_related(self):
        parent = ParentModel.objects.create(name='hello world')
        child = ChildModel.objects.create(number=5, parent=parent)
        result = ChildSerializer(instance=child).serialize(ignore_serializers=[ParentSerializer])
        self.assertIsNone(result['parent'])


    def test_serialize_fk_without_serializer(self):
        """
        If a related model is included but no serializer specified, then include the
        ids instead
        """
        parent = ParentModel.objects.create(name='perry')
        child = ChildModel.objects.create(number=2, parent=parent)
        ser = ChildModelSerializer(instance=child)
        data = ser.serialize()
        self.assertEqual(data['parent'], parent.pk)

    def test_serialize_reverse_fk_without_serializer(self):
        """
        If a related model is included but no serializer specified, then include the
        ids instead
        """
        parent = ParentModel.objects.create(name='perry')
        child_a = ChildModel.objects.create(number=2, parent=parent)
        child_b = ChildModel.objects.create(number=5, parent=parent)
        ser = ParentModelSerializer(instance=parent)
        data = ser.serialize()
        self.assertListEqual(list(data['childmodel_set']), [child_a.pk, child_b.pk])
