from ..route_handler import BaseModelRouter
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from swampdragon.tests.models import TextModel


class Serializer(ModelSerializer):
    class Meta:
        model = TextModel


class PaginatedRouter(BaseModelRouter):
    model = TextModel
    paginate_by = 5
    serializer_class = Serializer

    def get_query_set(self):
        return self.model.objects.all()


class TestBaseModelRouter(DragonTestCase):
    def setUp(self):
        self.router = PaginatedRouter(self.connection)
        for i in range(21):
            TextModel.objects.create(text='text {}'.format(i))

    def test_pagination(self):
        result = self.router.get_list()
        self.assertEqual(len(result), PaginatedRouter.paginate_by)

    def test_get_second_page(self):
        self.router.context['page'] = 2
        result = self.router.get_list()
        self.assertNotEqual(result[0].pk, 1)

    def test_get_last_page(self):
        self.router.context['page'] = 5
        result = self.router.get_list()
        self.assertEqual(len(result), 1)
