from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
from sockjs.tornado import SockJSConnection
from tornado import web
from ..pubsub_providers.redis_pubsub_provider import RedisPubSubProvider
from .. import route_handler
import json


class SubscriberConnection(SockJSConnection):
    def __init__(self, session):
        super(SubscriberConnection, self).__init__(session)

    def on_open(self, request):
        self.pub_sub = RedisPubSubProvider()

    def on_close(self):
        self.pub_sub.close()

    def _to_json(self, data):
        if isinstance(data, dict):
            return data
        try:
            data = json.loads(data.replace("'", '"'))
            return data
        except:
            return {'message': data}

    def on_message(self, data):
        data = self._to_json(data)
        handler = route_handler.get_route_handler(data['route'])
        handler(self).handle(data)

    def broadcast(self, clients, message):
        data = self._to_json(message)
        super(SubscriberConnection, self).broadcast(clients, data)

    def get(self):
        import ipdb;ipdb.set_trace()


class DjangoSubscriberConnection(SubscriberConnection):
    def get_user(self):
        if 'sessionid' not in self.session.handler.cookies:
            return AnonymousUser()
        session_id = self.session.handler.cookies['sessionid'].value
        try:
            session = Session.objects.get(session_key=session_id)
        except Session.DoesNotExist:
            return AnonymousUser()
        uid = session.get_decoded().get('_auth_user_id')
        try:
            user = get_user_model().objects.get(pk=uid)
            return user
        except get_user_model().DoesNotExist:
            return AnonymousUser()
