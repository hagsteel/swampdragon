from datetime import datetime
from django.db import models
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import TextModel, SDModel


class DateModel(SDModel):
    date = models.DateTimeField()


class DateModelSerializer(ModelSerializer):
    class Meta:
        model = DateModel
        publish_fields = ('date')
        update_fields = ('date')


class TextModelSerializer(ModelSerializer):
    class Meta:
        model = TextModel
        publish_fields = ('text')
        update_fields = ('text')


class TestModelSerializer(DragonTestCase):
    def test_deserialize_model(self):
        data = {'text': 'foo'}
        serializer = TextModelSerializer(data)
        model_instance = serializer.save()
        self.assertEqual(model_instance.text, data['text'])

    def test_passing_invalid_data(self):
        foo = 'text'
        with self.assertRaises(Exception):
            TextModelSerializer(foo)

    def test_ignore_non_model_fields(self):
        data = {'text': 'foo', 'random_field': 'val'}
        serializer = TextModelSerializer(data)
        model_instance = serializer.deserialize()
        self.assertEqual(model_instance.text, data['text'])

    def test_deserialize_field(self):
        date = datetime.now()
        data = {'date': str(date)}
        serializer = DateModelSerializer(data)
        object = serializer.save()
        self.assertEqual(object.date, date)
