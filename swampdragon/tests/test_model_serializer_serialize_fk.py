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
