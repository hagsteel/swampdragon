from .dragon_django_test_case import DragonDjangoTestCase
from .serializers import FooSerializer, BarSerializer, BazSerializer, QuxSerializer


class ObjectMapTest(DragonDjangoTestCase):
    def test_get_object_map(self):
        foo_graph = FooSerializer.get_object_map()
        bar_graph = BarSerializer.get_object_map()
        baz_graph = BazSerializer.get_object_map()
        qux_graph = QuxSerializer.get_object_map()
        