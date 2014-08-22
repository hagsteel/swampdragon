from sockjs.tornado import SockJSConnection
from ..pubsub_providers.subscriber_factory import get_subscription_provider
from .. import route_handler
import json


class ConnectionMixin(object):
    def to_json(self, data):
        """
        If the message is a dict, return it.
        If it's a string try to decode it into json,
        otherwise assume it's not a dictionary but a simple text message
        """
        if isinstance(data, dict):
            return data
        try:
            return json.loads(data)
        except:
            return {'message': data}


class SubscriberConnection(ConnectionMixin, SockJSConnection):
    channels = []
    pub_sub = None

    def __init__(self, session):
        super(SubscriberConnection, self).__init__(session)
        self.pub_sub = get_subscription_provider()

    def on_close(self):
        self.pub_sub.close(self)

    def on_message(self, data):
        try:
            data = self.to_json(data)
            handler = route_handler.get_route_handler(data['route'])
            handler(self).handle(data)
        except Exception as e:
            self.abort_connection()
            raise e

    def abort_connection(self):
        self.close()


class DjangoSubscriberConnection(SubscriberConnection):
    pass
