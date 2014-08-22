from django.db import models
from ..models import SelfPublishModel
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from .models import SDModel
from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter


class Document(SelfPublishModel, SDModel):
    content = models.TextField()
    serializer_class = 'DocumentSerializer'


class Person(SelfPublishModel, SDModel):
    name = models.CharField(max_length=100)
    documents = models.ManyToManyField(Document)
    serializer_class = 'PersonSerializer'


class DocumentSerializer(ModelSerializer):
    person_set = 'PersonSerializer'

    class Meta:
        model = Document


class PersonSerializer(ModelSerializer):
    documents = DocumentSerializer
    class Meta:
        model = Person


class PersonRouter(ModelRouter):
    route_name = 'people'
    serializer_class = PersonSerializer
    include_related = [DocumentSerializer]

    def get_object(self, **kwargs):
        return Person.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return Person.objects.all()


class TestSelfPubModel(DragonTestCase):
    def setUp(self):
        route_handler.register(PersonRouter)

    # def test_serialize_doc(self):
    #     doc = Document.objects.create(content='test', pk=99)
    #     person = Person.objects.create(name='a person')
    #     person.documents.add(doc)
    #     # import ipdb;ipdb.set_trace()
    #     serp = doc.serialize()
    #     import ipdb;ipdb.set_trace()


    def test_publish_m2m_on_add(self):
        self.connection.subscribe(PersonRouter.route_name, 'cli', {})
        Person.objects.create(name='some person')
        person = Person.objects.create(name='another person')
        person = Person.objects.get(pk=person.pk)
        doc = Document.objects.create(content='test', pk=99)
        self.connection.published_data = []
        # person.documents.add(doc)
        # import ipdb;ipdb.set_trace()
        # lp = self.connection.last_pub
        # self.assertListEqual(lp['data']['documents'], [doc.pk])

    def test_publish_m2m_on_remove(self):
        self.connection.subscribe(PersonRouter.route_name, 'cli', {})
        person = Person.objects.create(name='a person')
        doc = Document.objects.create(content='test', pk=100)
        person.documents.add(doc)
        self.connection.published_data = []
        person.documents.remove(doc)
        lp = self.connection.last_pub
