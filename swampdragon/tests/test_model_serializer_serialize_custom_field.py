from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import TextModel


class TextModelSerializer(ModelSerializer):
    class Meta:
        model = TextModel
        publish_fields = ('text', 'custom_field')

    def serialize_custom_field(self, obj, serializer):
        return 'data'


class TestModelSerializer(DragonTestCase):
    def test_serialize_custom_field(self):
        text_model = TextModel.objects.create(text='hello world')
        result = TextModelSerializer(instance=text_model).serialize()
        self.assertEqual(result['custom_field'], 'data')