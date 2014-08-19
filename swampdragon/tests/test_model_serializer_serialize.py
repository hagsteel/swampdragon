from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import TextModel, ChildModel, ParentModel


class TextModelSerializer(ModelSerializer):
    class Meta:
        model = TextModel
        publish_fields = ('text', )
        base_channel = 'custom_base_channel'


class TestModelSerializer(DragonTestCase):
    def test_serialize_model(self):
        text_model = TextModel.objects.create(text='hello world')
        serializer = TextModelSerializer(instance=text_model)
        data = serializer.serialize()
        self.assertEqual(text_model.pk, data['id'])
        self.assertEqual(text_model.text, data['text'])

    def test_serializer_without_instance(self):
        """
        Serializing without instance should return None
        """
        expected = None
        actual = TextModelSerializer().serialize()
        self.assertEqual(expected, actual)

    def test_serialize_custom_base_channel(self):
        self.assertEqual(TextModelSerializer.get_base_channel(), 'custom_base_channel|')
