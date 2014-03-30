import json
import uuid
from .mock_provider import MockProvider
from .connection_pool import add_connection
from .models import TestUser


class TestConnection(object):
    uid = None

    def __init__(self):
        self.uid = str(uuid.uuid4())
        add_connection(self)

        self.sent_data = []
        self.pub_sub = MockProvider()

    def send(self, message):
        self.sent_data.append(json.dumps(message))


class TestConnectionWithUser(TestConnection):
    def __init__(self, user=None):
        super(TestConnectionWithUser, self).__init__()
        if user is None:
            self.user = TestUser()
        else:
            self.user = user

    def get_user(self, **kwargs):
        return self.user
