from swampdragon import route_handler
from swampdragon.route_handler import BaseModelRouter
from swampdragon.testing.dragon_testcase import DragonTestCase
from .models import DRFModel
from .serializers_drf import DRFSerializer


class Router(BaseModelRouter):
    route_name = 'model-router'
    model = DRFModel
    serializer_class = DRFSerializer

    def get_object(self, **kwargs):
        return self.model.objects.first()

    def get_query_set(self, **kwargs):
        return self.model.objects.all()


class TestDRFSerializer(DragonTestCase):
    def setUp(self):
        super(TestDRFSerializer, self).setUp()
        route_handler.register(Router)

    def test_drf_serializes_with_route_handler(self):
        DRFModel.objects.create(name='drf test')
        self.connection.call_verb(Router.route_name, 'get_single')
        self.assertDictEqual(self.connection.last_message['data'], {'name': 'drf test', 'id': 1})

    def test_deserialize_drf_with_route_handler(self):
        self.connection.call_verb(Router.route_name, 'create', name='creating')
        self.assertTrue(DRFModel.objects.exists())
