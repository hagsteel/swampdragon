from django_webtest import WebTest
from ..pubsub_providers.channel_utils import filter_matching_channels
from ..serializers.base_serializer import BaseSerializer
from .mock_connection import TestConnection


class TestObject(object):
    def __init__(self, name, numval):
        super(TestObject, self).__init__()
        self.name = name
        self.numval = numval


class TestObjectSerializer(BaseSerializer):
    publish_fields = ['name', 'numval']


class PubSubTest(WebTest):
    def test_subscribe_to_all_test_objects(self):
        connection = TestConnection()
        channel = 'test_chan'
        connection.pub_sub.subscribe(channel, connection)
        test_object = TestObject('foo', 1)
        connection.pub_sub.publish(channel, TestObjectSerializer().serialize(test_object))
        test_object = TestObject('bar', 2)
        connection.pub_sub.publish(channel, TestObjectSerializer().serialize(test_object))
        self.assertEqual(len(connection.pub_sub._subscribers.keys()), 1)

    def test_filter_matching_channels(self):
        channels = [
            'TestObject|name__contains:foo',
            'TestObject|name__contains:bar',
        ]
        matched_channels = filter_matching_channels(channels, data={'name': 'fooo'})
        self.assertEqual(matched_channels[0], channels[0])
        self.assertEqual(len(matched_channels), 1)
        matched_channels = filter_matching_channels(channels, data={'name': 'barr'})
        self.assertEqual(matched_channels[0], channels[1])
        self.assertEqual(len(matched_channels), 1)
        matched_channels = filter_matching_channels(channels, data={'name': 'foobar'})
        self.assertEqual(len(matched_channels), 2)
