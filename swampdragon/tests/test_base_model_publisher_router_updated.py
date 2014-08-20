from ..route_handler import BaseModelPublisherRouter
from ..serializers.model_serializer import ModelSerializer
from .dragon_test_case import DragonTestCase
from ..pubsub_providers.base_provider import PUBACTIONS
from .models import TwoFieldModel


class Serializer(ModelSerializer):
    class Meta:
        publish_fields = ('text', 'number')
        update_fields = ('text', 'number')
        model = TwoFieldModel


class Router(BaseModelPublisherRouter):
    model = TwoFieldModel
    serializer_class = Serializer

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_subscription_contexts(self, **kwargs):
        if 'number' in kwargs:
            return {'number': kwargs['number']}
        return {}


class TestBaseModelPublisherRouter(DragonTestCase):
    def setUp(self):
        self.router = Router(self.connection)
        self.obj = self.router.model.objects.create(text='text', number=123)

    def test_updated(self):
        data = {'text': 'text', 'number': 3, 'id': self.obj.pk}
        self.router.update(**data)
        model = self.router.model.objects.get()
        self.assertEqual(model.number, data['number'])

    def test_updated_publish(self):
        self.router.subscribe(**{'channel': 'client-channel'})
        data = {'text': 'text', 'number': 3, 'id': self.obj.pk}
        self.router.update(**data)
        actual = self.connection.get_last_published()
        expected = {'action': 'updated', 'channel': 'twofieldmodel|', 'data': {'_type': 'twofieldmodel', 'id': 1, 'number': 3}}
        self.assertDictEqual(actual, expected)

    def test_updated_remove_from_channel(self):
        """
        When a model no longer match the channel the subscriber should
        receive a DELETE action
        """
        self.router.subscribe(**{'channel': 'client-channel', 'number': 2})
        data = {'text': 'text', 'number': 2, 'id': self.obj.pk}
        self.router.update(**data)
        self.assertEqual(self.connection.last_pub['action'], PUBACTIONS.updated)

        data = {'text': 'text', 'number': 200, 'id': self.obj.pk}
        self.router.update(**data)
        self.assertEqual(self.connection.last_pub['action'], PUBACTIONS.deleted)

