from swampdragon.serializers.model_serializer import ModelSerializer
from swampdragon.testing.dragon_testcase import DragonTestCase
from .models import TextModel, SDModel
from datetime import datetime
from django.db import models


# to make sure none of the ModelSerializer variables are clobbering the data
MODEL_KEYWORDS = ('data', )
# TODO: support the rest of these field names
# MODEL_KEYWORDS = ('data', 'opts', 'initial', 'base_fields', 'm2m_fields', 'related_fields', 'errors')


class KeywordModel(SDModel):
    data = models.TextField()
    # TODO: support the rest of these field names
    # opts = models.TextField()
    # initial = models.TextField()
    # base_fields = models.TextField()
    # m2m_fields = models.TextField()
    # related_fields = models.TextField()
    # errors = models.TextField()


class KeywordModelSerializer(ModelSerializer):
    class Meta:
        model = KeywordModel
        publish_fields = MODEL_KEYWORDS
        update_fields = MODEL_KEYWORDS


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

    def test_deserialize_keyword_field(self):
        data = dict(zip(MODEL_KEYWORDS, MODEL_KEYWORDS))
        serializer = KeywordModelSerializer(data)
        object = serializer.save()
        for attr in MODEL_KEYWORDS:
            self.assertEqual(getattr(object, attr), attr)
