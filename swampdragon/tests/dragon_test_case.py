from unittest import TestCase
from . import mock_provider
from swampdragon import discover_routes
from swampdragon.models import SelfPublishModel
from swampdragon.tests.mock_connection import TestConnection
from swampdragon.tests.mock_provider import MockPubSubProvider


class DragonTestCase(TestCase):
    is_patched = False

    def __init__(self, methodName='runTest'):
        super(DragonTestCase, self).__init__(methodName)
        self.patch_pubsub()
        mock_provider._channels = []
        mock_provider._subscribers = {}
        self.connection = TestConnection()
        discover_routes()

    def tearDown(self):
        mock_provider._channels = []
        mock_provider._subscribers = {}

    def patch_pubsub(self):
        if self.is_patched:
            return
        SelfPublishModel.publisher_class = MockPubSubProvider
        self.is_patched = True