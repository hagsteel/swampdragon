import json
from .. import route_handler
from ..route_handler import BaseModelPublisherRouter, UnexpectedVerbException
from ..serializers.model_serializer import ModelSerializer
from ..tests import ParentModel, ChildModel, SubChildModel
from .mock_connection import TestConnection
from .dragon_django_test_case import DragonDjangoTestCase
from .models import FooModel, BarModel
from .serializers import FooSerializer


class FooRouter(BaseModelPublisherRouter):
    valid_verbs = BaseModelPublisherRouter.valid_verbs + ['get_misc_data']
    model = FooModel
    route_name = 'test_parent_router'
    serializer_class = FooSerializer
    # include_related = [ChildModelSerializer, SubChildModelSerializer]

    def get_query_set(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def get_object(self, **kwargs):
        return self.model.objects.get(id=kwargs['id'])

    def get_misc_data(self, **kwargs):
        self.send({'foo': 'bar'})



class TestModelRouter(DragonDjangoTestCase):
    def setUp(self):
        route_handler.register(FooRouter)
        # route_handler.register(ChildRouter)
        # route_handler.register(SubChildRouter)
        self.connection = TestConnection()
        self.foo_router = route_handler.get_route_handler(FooRouter.route_name)
        # self.child_handler = route_handler.get_route_handler(ChildRouter.route_name)
        # self.subchild_handler = route_handler.get_route_handler(SubChildRouter.route_name)

    def test_subscribe(self):
        '''
        Subscribe to a channel
        '''
        data = {'verb': 'subscribe', 'args': {'channel': 'testchan'}}
        self.foo_router(self.connection).handle(data)
        data = self.connection.get_last_message()['data']

        self.assertListEqual(
            data,
            self.foo_router.serializer_class.get_object_map(self.foo_router.include_related)
        )

        remote_channels = json.loads(self.connection.sent_data[0])['channel_data']['remote_channels']
        for channel in remote_channels:
            self.assertTrue(self.connection in self.connection.pub_sub._subscribers[channel])

    def test_unsubscribe(self):
        '''
        Unsubscribe to a channel
        '''
        data = {'verb': 'subscribe', 'args': {'channel': 'testchan'}}
        self.foo_router(self.connection).handle(data)
        data = {'verb': 'unsubscribe', 'args': {'channel': 'testchan'}}
        self.foo_router(self.connection).handle(data)

        received_data = self.connection.get_last_message()

        self.assertEqual(received_data['data'], 'unsubscribed')
        remote_channels = received_data['channel_data']['remote_channels']
        for channel in remote_channels:
            self.assertTrue(self.connection not in self.connection.pub_sub._subscribers.get(channel, []))

    def test_create_model(self):
        model_data = {'test_field_a': 'test data', 'test_field_b': 'foo test'}
        data = {'verb': 'create', 'args': model_data}
        self.foo_router(self.connection).handle(data)
        self.assertTrue(self.foo_router.model.objects.filter(**model_data).exists())

    def test_update_model(self):
        model_data = {'test_field_a': 'value'}
        foo = FooModel.objects.create(**model_data)

        update_data = {
            'id': foo.pk,
            'test_field_a': 'updated data'
        }

        data = {'verb': 'update', 'args': update_data}
        self.foo_router(self.connection).handle(data)
        updated_model = self.foo_router.model.objects.get(**{'pk': foo.pk})
        self.assertEqual(foo.pk, updated_model.pk)
        self.assertEqual(updated_model.test_field_a, 'updated data')

    def test_delete_model(self):
        foo_model = FooModel.objects.create(**{'test_field_a': 'test parent', 'test_field_b': '55'})
        data = {'verb': 'delete', 'args': {'id': foo_model.id}}
        self.foo_router(self.connection).handle(data)
        self.assertFalse(self.foo_router.model.objects.filter(**{'id': foo_model.id}).exists())

    def test_get_models(self):
        model_data = {'test_field_a': 'test', 'test_field_b': 'testing'}
        foo = FooModel.objects.create(**model_data)
        data = {'verb': 'get_list', 'args': {'id': foo.id}}
        self.foo_router(self.connection).handle(data)
        actual_data = self.connection.get_last_message()['data'][0]
        expected_data = FooSerializer(instance=foo).serialize()
        for ed in actual_data.keys():
            self.assertEqual(expected_data[ed], actual_data[ed])

    def test_get_model(self):
        foo = FooModel.objects.create(**{'test_field_a': 'test', 'test_field_b': '123 test'})
        data = {'verb': 'get_single', 'args': {'id': foo.id}}
        self.foo_router(self.connection).handle(data)
        expected_data = FooSerializer(instance=foo).serialize()
        actual_data = self.connection.get_last_message()['data']
        for ed in expected_data.keys():
            self.assertEqual(expected_data[ed], actual_data[ed])

    def test_unexpected_verb_exception(self):
        with self.assertRaises(UnexpectedVerbException):
            data = {'verb': 'madeupverb'}
            self.foo_router(self.connection).handle(data)

    def test_get_parents_with_children(self):
        foo = FooModel.objects.create(test_field_a='hello', test_field_b='world',)
        BarModel.objects.create(number=12, foo=foo)

        data = {'verb': 'get_list'}
        self.foo_router(self.connection).handle(data)
        received_data = self.connection.get_last_message()['data']
        self.assertEqual(len(received_data[0]['bars']), 1)

    def test_get_parent_with_children(self):
        foo = FooModel.objects.create(test_field_a='hello', test_field_b='world',)
        BarModel.objects.create(number=12, foo=foo)

        data = {'verb': 'get_single', 'args': {'id': foo.pk}}
        self.foo_router(self.connection).handle(data)
        received_data = self.connection.get_last_message()['data']
        self.assertEqual(len(received_data['bars']), 1)

    def test_get_models_with_filter(self):
        FooModel.objects.create(test_field_a='hello', test_field_b='world',)
        foo = FooModel.objects.create(test_field_a='findme', test_field_b='world',)
        data = {'verb': 'get_list', 'args': {'test_field_a__contains': 'find'}}
        # data = {'verb': 'get_list'}
        self.foo_router(self.connection).handle(data)
        received_data = self.connection.get_last_message()
        self.assertTrue(len(received_data), 1)
        self.assertEqual(received_data['data'][0]['test_field_a'], foo.test_field_a)

    # def test_subscribe_to_related(self):
    #     parent = ParentModel.objects.create(name='foo', age=55)
    #     kwargs = {'channel': 'client_chan', 'parent_id': parent.pk, }
    #     self.parent_handler(self.connection).subscribe(**kwargs)
    #     expected_channels = [
    #         '{}parent_id:1'.format(ParentModelSerializer.get_base_channel()),
    #         '{}parent__parent_id:1'.format(ChildModelSerializer.get_base_channel()),
    #         '{}child__parent__parent_id:1'.format(SubChildModelSerializer.get_base_channel()),
    #     ]
    #     json_data = json.loads(self.connection.sent_data[-1])
    #     remote_channels = json_data['channel_data']['remote_channels']
    #     self.assertListEqual(remote_channels, expected_channels)

    def test_custom_get_method(self):
        FooModel.objects.create(test_field_a='hello', test_field_b='world',)
        FooModel.objects.create(test_field_a='foo', test_field_b='bar',)
        FooModel.objects.create(test_field_a='baz', test_field_b='qux',)
        data = {'verb': 'get_misc_data'}
        self.foo_router(self.connection).handle(data)
        data = self.connection.get_last_message()['data']
        self.assertDictEqual(data, {'foo': 'bar'})
#
#     def test_remove_on_update(self):
#         parent = ParentModel.objects.create(name='foo', age=55)
#         kwargs = {'channel': 'client_chan', 'name': 'foo', }
#         self.parent_handler(self.connection).subscribe(**kwargs)
#         self.parent_handler(self.connection).update(**{'id': parent.pk, 'name': 'updated'})
#         last_update = self.connection.get_last_published()
#         self.assertEqual(last_update['action'], 'deleted')
#
#     def test_specify_related_models_on_subscribe(self):
#         self.parent_handler(self.connection).subscribe(**{'channel': 'parent', 'id': 1})
#         obj_map = json.loads(self.connection.sent_data[-1])['data']
#         self.assertEqual(len(obj_map), 2)
#         self.assertEqual(len(self.connection.pub_sub._channels), 3)

