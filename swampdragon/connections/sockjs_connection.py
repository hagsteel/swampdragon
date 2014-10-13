from sockjs.tornado import SockJSConnection
from tornado.ioloop import PeriodicCallback
from ..pubsub_providers.subscriber_factory import get_subscription_provider
from .. import route_handler
from ..sessions.sessions import get_session_store
import json


session_store = get_session_store()


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
    pub_sub = None

    def __init__(self, session):
        super(SubscriberConnection, self).__init__(session)
        self.session_store = session_store(self.session.session_id)
        self.pub_sub = get_subscription_provider()

    def on_open(self, request):
        super(SubscriberConnection, self).on_open(request)
        session_key_timeout_seconds = 1000 * 60 * 20  # 20 minutes
        self.periodic_callback = PeriodicCallback(self.on_heartbeat, session_key_timeout_seconds)
        self.periodic_callback.start()

    def on_heartbeat(self):
        self.session_store.refresh_all_keys()

    def on_close(self):
        self.periodic_callback.stop()
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
