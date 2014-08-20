from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import TextModel, ParentModel, ChildModel


class TextModelSerializer(ModelSerializer):
    class Meta:
        model = TextModel
        publish_fields = ('text', 'custom_field')

    def serialize_custom_field(self, obj):
        return 'data'


class CustomTextModelSerializer(ModelSerializer):
    class Meta:
        model = TextModel

    def serialize_foo(self, obj):
        return 'bar'


class ChildSerializer(ModelSerializer):
    class Meta:
        model = ChildModel


class RelatedSerializer(ModelSerializer):
    childmodel_set = 'ChildSerializer'

    class Meta:
        model = ParentModel

    def serialize_childmodel_set(self, obj, serializer):
        return 'c {}'.format(serializer(instance=obj.childmodel_set.first()).serialize()['id'])


class TestModelSerializer(DragonTestCase):
    def test_serialize_custom_field(self):
        text_model = TextModel.objects.create(text='hello world')
        result = TextModelSerializer(instance=text_model).serialize()
        self.assertEqual(result['custom_field'], 'data')

    def test_serialize_custom_field_not_in_publish_fields(self):
        text_model = TextModel.objects.create(text='hello world')
        result = CustomTextModelSerializer(instance=text_model).serialize()
        self.assertEqual(result['foo'], 'bar')

    def test_serialize_custom_related(self):
        parent = ParentModel.objects.create(name='foo')
        child = ChildModel.objects.create(number=19, parent=parent)
        data = RelatedSerializer(instance=parent).serialize()
        self.assertEqual(data['childmodel_set'], 'c {}'.format(child.pk))
