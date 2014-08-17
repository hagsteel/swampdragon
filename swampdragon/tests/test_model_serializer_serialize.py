from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import TextModel


class TextModelSerializer(ModelSerializer):
    class Meta:
        model = TextModel
        publish_fields = ('text', )


class TestModelSerializer(DragonTestCase):
    def test_serialize_model(self):
        text_model = TextModel.objects.create(text='hello world')
        serializer = TextModelSerializer(instance=text_model)
        data = serializer.serialize()
        self.assertEqual(text_model.pk, data['id'])
        self.assertEqual(text_model.text, data['text'])
