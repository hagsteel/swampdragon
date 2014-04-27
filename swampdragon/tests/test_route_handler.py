import json
from .. import route_handler
from ..route_handler import BaseModelPublisherRouter, UnexpectedVerbException
from ..serializers.django_model_serializer import DjangoModelSerializer
from ..tests import ParentModel, ChildModel, SubChildModel
from .mock_connection import TestConnection
from .dragon_django_test_case import DragonDjangoTestCase


class ChildModelSerializer(DjangoModelSerializer):
    model = ChildModel
    publish_fields = ['name', 'id', 'parent_id', 'subchildren']
    update_fields = ['name', 'parent_id']

    def serialize_subchildren(self, obj, **kwargs):
        return [SubChildModelSerializer().serialize(c) for c in obj.subchildren.all()]


class SubChildModelSerializer(DjangoModelSerializer):
    model = SubChildModel
    publish_fields = ['name', 'id', 'child_id']
    update_fields = ['name', 'child_id']


class ParentModelSerializer(DjangoModelSerializer):
    model = ParentModel
    publish_fields = ['name', 'age', 'id', 'children']
    update_fields = ['name', 'age']

    def serialize_children(self, obj, **kwargs):
        children = [ChildModelSerializer().serialize(c) for c in obj.children.all()]
        return children


class ParentRouter(BaseModelPublisherRouter):
    valid_verbs = BaseModelPublisherRouter.valid_verbs + ['get_foo_parents']
    model = ParentModel
    route_name = 'test_parent_router'
    serializer_class = ParentModelSerializer
    include_related = [ChildModelSerializer, SubChildModelSerializer]

    def get_query_set(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def get_object(self, **kwargs):
        return self.model.objects.get(id=kwargs['id'])

    def get_foo_parents(self, **kwargs):
        parents = self.model.objects.filter(name__contains='foo')
        self.send_list(parents, **kwargs)


class ChildRouter(BaseModelPublisherRouter):
    model = ChildModel
    route_name = 'test_child_router'
    serializer_class = ChildModelSerializer

    def get_query_set(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def get_object(self, **kwargs):
        return self.model.objects.get(**kwargs)


class SubChildRouter(BaseModelPublisherRouter):
    model = SubChildModel
    route_name = 'test_subchild_router'
    serializer_class = SubChildModelSerializer

    def get_query_set(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def get_object(self, **kwargs):
        return self.model.objects.get(**kwargs)


class TestModelRouter(DragonDjangoTestCase):
    def setUp(self):
        route_handler.register(ParentRouter)
        route_handler.register(ChildRouter)
        route_handler.register(SubChildRouter)
        self.connection = TestConnection()
        self.parent_handler = route_handler.get_route_handler(ParentRouter.route_name)
        self.child_handler = route_handler.get_route_handler(ChildRouter.route_name)
        self.subchild_handler = route_handler.get_route_handler(SubChildRouter.route_name)

    def test_subscribe(self):
        data = {'verb': 'subscribe', 'args': {'channel': 'testchan'}}
        self.parent_handler(self.connection).handle(data)
        self.assertListEqual(
            json.loads(self.connection.sent_data[0])['data'],
            self.parent_handler.serializer_class.get_object_map(self.parent_handler.include_related)
        )
        remote_channels = json.loads(self.connection.sent_data[0])['channel_data']['remote_channels']
        for channel in remote_channels:
            self.assertTrue(self.connection in self.connection.pub_sub._subscribers[channel])

    def test_unsubscribe(self):
        data = {'verb': 'subscribe', 'args': {'channel': 'testchan'}}
        self.parent_handler(self.connection).handle(data)
        data = {'verb': 'unsubscribe', 'args': {'channel': 'testchan'}}
        self.parent_handler(self.connection).handle(data)
        self.assertEqual(json.loads(self.connection.sent_data[-1])['data'], 'unsubscribed')
        remote_channels = json.loads(self.connection.sent_data[-1])['channel_data']['remote_channels']
        for channel in remote_channels:
            self.assertTrue(self.connection not in self.connection.pub_sub._subscribers.get(channel, []))

    def test_create_model(self):
        model_data = {'name': 'test parent', 'age': 55}
        data = {'verb': 'create', 'args': model_data}
        self.parent_handler(self.connection).handle(data)
        self.assertTrue(ParentRouter.model.objects.filter(**model_data).exists())

    def test_update_model(self):
        model_data = {'name': 'test parent', 'age': 55}
        parent_model = ParentModel.objects.create(**model_data)

        update_data = {
            'id': parent_model.id,
            'name': 'updated_parent'
        }

        data = {'verb': 'update', 'args': update_data}
        self.parent_handler(self.connection).handle(data)
        updated_model = ParentRouter.model.objects.get(**{'id': parent_model.id})
        self.assertEqual(parent_model.id, updated_model.id)

    def test_delete_model(self):
        parent_model = ParentModel.objects.create(**{'name': 'test parent', 'age': 55})
        data = {'verb': 'delete', 'args': {'id': parent_model.id}}
        self.parent_handler(self.connection).handle(data)
        self.assertFalse(ParentRouter.model.objects.filter(**{'id': parent_model.id}).exists())

    def test_get_models(self):
        parent_model = ParentModel.objects.create(**{'name': 'test parent', 'age': 55})
        data = {'verb': 'get_list', 'args': {'id': parent_model.id}}
        self.parent_handler(self.connection).handle(data)
        expected_data = {
            'name': 'test parent',
            'age': 55
        }
        actual_data = json.loads(self.connection.sent_data[0])['data'][0]
        for ed in expected_data.keys():
            self.assertEqual(expected_data[ed], actual_data[ed])

    def test_get_model(self):
        parent_model = ParentModel.objects.create(**{'name': 'test parent', 'age': 55})
        data = {'verb': 'get_single', 'args': {'id': parent_model.id}}
        self.parent_handler(self.connection).handle(data)
        expected_data = {
            'name': 'test parent',
            'age': 55
        }
        actual_data = json.loads(self.connection.sent_data[0])['data']
        for ed in expected_data.keys():
            self.assertEqual(expected_data[ed], actual_data[ed])

    def test_unexpected_verb_exception(self):
        with self.assertRaises(UnexpectedVerbException):
            data = {'verb': 'madeupverb'}
            self.parent_handler(self.connection).handle(data)

    def test_get_parents_with_children(self):
        parent_model = ParentModel.objects.create(**{'name': 'test parent', 'age': 55})
        ChildModel.objects.create(**{'name': 'test parent', 'parent_id': parent_model.pk})

        data = {'verb': 'get_list'}
        self.parent_handler(self.connection).handle(data)
        received_data = json.loads(self.connection.sent_data[0])['data']
        self.assertEqual(len(received_data[0]['children']), 1)

    def test_get_parent_with_children(self):
        parent_model = ParentModel.objects.create(**{'name': 'test parent', 'age': 55})
        ChildModel.objects.create(**{'name': 'test parent', 'parent_id': parent_model.pk})

        data = {'verb': 'get_single', 'args': {'id': parent_model.id}}
        self.parent_handler(self.connection).handle(data)
        received_data = json.loads(self.connection.sent_data[0])['data']
        self.assertEqual(len(received_data['children']), 1)

    def test_get_parent_with_children_and_subchildren(self):
        parent_model = ParentModel.objects.create(**{'name': 'test parent', 'age': 55})
        child_model = ChildModel.objects.create(**{'name': 'test child', 'parent_id': parent_model.pk})
        SubChildModel.objects.create(**{'name': 'test subchild', 'child_id': child_model.pk})

        data = {'verb': 'get_single', 'args': {'id': parent_model.id}}
        self.parent_handler(self.connection).handle(data)
        received_data = json.loads(self.connection.sent_data[0])['data']
        self.assertEqual(len(received_data['children']), 1)
        self.assertEqual(len(received_data['children'][0]['subchildren']), 1)

    def test_get_models_with_filter(self):
        ParentModel.objects.create(**{'name': 'test parent a', 'age': 55})
        ParentModel.objects.create(**{'name': 'test parent b', 'age': 55})
        parent_model_c = ParentModel.objects.create(**{'name': 'other', 'age': 55})
        data = {'verb': 'get_list', 'args': {'name__contains': 'test'}}
        self.parent_handler(self.connection).handle(data)
        received_data = json.loads(self.connection.sent_data[0])['data']
        self.assertTrue(len(received_data), 2)
        for p in received_data:
            self.assertNotEqual(p['name'], parent_model_c.name)

    def test_subscribe_to_related(self):
        parent = ParentModel.objects.create(name='foo', age=55)
        kwargs = {'channel': 'client_chan', 'parent_id': parent.pk, }
        self.parent_handler(self.connection).subscribe(**kwargs)
        expected_channels = [
            '{}parent_id:1'.format(ParentModelSerializer.get_base_channel()),
            '{}parent__parent_id:1'.format(ChildModelSerializer.get_base_channel()),
            '{}child__parent__parent_id:1'.format(SubChildModelSerializer.get_base_channel()),
        ]
        json_data = json.loads(self.connection.sent_data[-1])
        remote_channels = json_data['channel_data']['remote_channels']
        self.assertListEqual(remote_channels, expected_channels)

    def test_custom_get_method(self):
        ParentModel.objects.create(name='foo_a', age=55)
        ParentModel.objects.create(name='foo_b', age=55)
        ParentModel.objects.create(name='bar', age=55)
        data = {'verb': 'get_foo_parents', 'args': {}}
        self.parent_handler(self.connection).handle(data)
        json_data = json.loads(self.connection.sent_data[-1])['data']
        self.assertEqual(len(json_data), 2)
        for parent in json_data:
            self.assertTrue('foo' in parent['name'])
            self.assertTrue('bar' not in parent['name'])

    def test_remove_on_update(self):
        parent = ParentModel.objects.create(name='foo', age=55)
        kwargs = {'channel': 'client_chan', 'name': 'foo', }
        self.parent_handler(self.connection).subscribe(**kwargs)
        self.parent_handler(self.connection).update(**{'id': parent.pk, 'name': 'updated'})
        last_update = self.connection.get_last_published()
        self.assertEqual(last_update['action'], 'deleted')

    def test_specify_related_models_on_subscribe(self):
        self.parent_handler(self.connection).subscribe(**{'channel': 'parent', 'id': 1})
        obj_map = json.loads(self.connection.sent_data[-1])['data']
        self.assertEqual(len(obj_map), 2)
        self.assertEqual(len(self.connection.pub_sub._channels), 3)
