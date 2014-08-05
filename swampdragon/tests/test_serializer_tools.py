from .dragon_django_test_case import DragonDjangoTestCase
from ..serializers.serializer_tools import get_serializer_relationship_field
from .serializers import FooSerializer, BarSerializer, StaffSerializer, DocumentSerializer


class SerializerTest(DragonDjangoTestCase):
    def test_get_serializer_relationship_m2m(self):
        rel = get_serializer_relationship_field(DocumentSerializer, StaffSerializer)
        self.assertEqual(rel, 'document')

    def test_get_serializer_relationship_reverse_m2m(self):
        rel = get_serializer_relationship_field(StaffSerializer, DocumentSerializer)
        self.assertEqual(rel, 'staff')

    def test_get_serializser_relationship_with_reverse_fk(self):
        rel = get_serializer_relationship_field(FooSerializer, BarSerializer)
        self.assertEqual(rel, 'foo')

    def test_get_serializser_relationship_with_fk(self):
        rel = get_serializer_relationship_field(BarSerializer, FooSerializer)
        self.assertEqual(rel, 'barmodel')
