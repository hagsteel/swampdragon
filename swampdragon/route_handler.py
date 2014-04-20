import json
from tornado.web import RequestHandler
from .pubsub_providers.base_provider import PUBACTIONS
from .message_format import format_message
from .pubsub_providers.model_channel_builder import make_channels, filter_channels_by_model
from .pubsub_providers.model_publisher import publish_model
from .file_upload_handler import get_file_location, get_file_url, make_file_id

registered_handlers = {}


class UnexpectedVerbException(Exception):
    pass


class FileUploadHandler(RequestHandler):
    def _set_access_control(self):
        origin = self.request.headers['origin']
        orig_test = origin.split('/')[-1]
        if ':' in orig_test:
            orig_test= orig_test.split(':')[0]
        if not self.request.host.split(':')[0] == orig_test:
            return
        self.set_header('Access-Control-Allow-Credentials', True)
        self.set_header('Access-Control-Allow-Methods', 'POST')
        self.set_header('Access-Control-Allow-Origin', origin)

    def get(self, *args, **kwargs):
        self.write('Hello!')

    def post(self, *args, **kwargs):
        self._set_access_control()
        files = self.request.files['uploadedFile']
        response = {'files': []}
        for f in files:
            file_id = make_file_id(f['body'])
            file_name = f['filename']
            named_file = open(get_file_location(file_name, file_id), 'w')
            named_file.write(f['body'])
            named_file.close()
            response['files'].append({
                'file_id': file_id,
                'file_name': file_name,
                'file_url': get_file_url(file_name, file_id)
            })
        self.write(json.dumps(response))

    def options(self, *args, **kwargs):
        self._set_access_control()

    def file_upload(self, request):
        pass


class BaseRouter(FileUploadHandler):
    valid_verbs = ['get_list', 'get_single', 'create', 'update', 'delete', 'subscribe', 'unsubscribe']
    serializer_class = None
    serializer = None
    route_name = None
    permission_classes = []

    def __init__(self, connection, request=None, **kwargs):
        if request is not None:
            super(BaseRouter, self).__init__(connection, request, **kwargs)
        if request:
            # This is a normal web request so we won't have a connection
            return
        else:
            self.connection = connection
        self.context = dict()

    def make_channel_data(self, client_channel, server_channels):
        return {'local_channel': client_channel, 'remote_channels': server_channels}

    @classmethod
    def get_name(cls):
        try:
            return getattr(cls, 'route_name')
        except AttributeError:
            raise Exception('\n------\n{} has no name.\nSet the route_name property\n------\n'.format(cls.__name__))

    def handle(self, data):
        verb = data['verb']
        kwargs = data.get('args', {})
        client_callback_name = data.get('callbackname')
        self.context['client_callback_name'] = client_callback_name,
        if verb in self.valid_verbs:
            m = getattr(self, verb)
            if self.permission_classes:
                for permission in self.permission_classes:
                    if not permission.test_permission(self, verb, **kwargs):
                        permission.permission_failed(self)
                        return
            m(**kwargs)
        else:
            raise UnexpectedVerbException('\n------\nUnexpected verb: {}\n------'.format(verb))

    def get_list(self, **kwargs):
        raise NotImplemented()

    def got_list(self, **kwargs):
        raise NotImplemented()

    def get_single(self, **kwargs):
        raise NotImplemented()

    def create(self, **kwargs):
        raise NotImplemented()

    def created(self, obj):
        raise NotImplemented()

    def update(self, **kwargs):
        raise NotImplemented()

    def updated(self, obj, **kwargs):
        raise NotImplemented()

    def delete(self, **kwargs):
        raise NotImplemented()

    def deleted(self, obj, **kwargs):
        raise NotImplemented()

    def get_initials(self, verb, **kwargs):
        return dict()

    def send(self, data, channel_setup=None):
        self.context['state'] = 'success'
        message = format_message(data=data, context=self.context, channel_setup=channel_setup)
        self.connection.send(message)

    def send_error(self, data, channel_setup=None):
        self.context['state'] = 'error'
        self.connection.send(format_message(data=data, context=self.context, channel_setup=channel_setup))

    def send_login_required(self, channel_setup=None):
        self.context['state'] = 'login_required'
        self.connection.send(format_message(data=None, context=self.context, channel_setup=channel_setup))

    def get_subscription_channels(self, **kwargs):
        raise NotImplemented()

    def subscribe(self, **kwargs):
        client_channel = kwargs.pop('channel')
        server_channels = self.get_subscription_channels(**kwargs)
        self.send(data='subscribed', channel_setup=self.make_channel_data(client_channel, server_channels))
        self.connection.pub_sub.subscribe(server_channels, self.connection)

    def unsubscribe(self, **kwargs):
        client_channel = kwargs.pop('channel')
        server_channels = self.get_subscription_channels(**kwargs)
        self.send(data='unsubscribed', channel_setup=self.make_channel_data(client_channel, server_channels))
        self.connection.pub_sub.unsubscribe(server_channels, self.connection)

    def publish(self, channels, publish_data):
        for channel in channels:
            publish_data['channel'] = channel
            self.connection.pub_sub.publish(channel, publish_data)

    def get_subscription_context(self, **kwargs):
        return dict(kwargs)

def replace_original_with_data(kwargs):
    keys = [key for key in kwargs.keys() if '__' in key]
    for key in keys:
        val = kwargs.pop(key)
        kwargs[key.split('__')[0]] = val
    return kwargs


class BaseModelRouter(BaseRouter):
    model = None
    instance = None

    def _get_changes(self, current_state, past_state):
        changed_state = {}

        for o in current_state:
            if past_state[o] != current_state[o]:
                changed_state[o] = current_state[o]
        if self.serializer.id_field not in changed_state:
            changed_state[self.serializer.id_field] = current_state[self.serializer.id_field]
        return changed_state

    def get_query_set(self, **kwargs):
        raise NotImplemented('Implement get_query_set in your handler')

    def get_object(self, **kwargs):
        raise NotImplemented('Implement get_object in your handler')

    def get_list(self, **kwargs):
        obj_list = self.get_query_set(**kwargs)
        self.send_list(obj_list, **kwargs)
        return obj_list

    def send_list(self, object_list, **kwargs):
        self.serializer = self.serializer_class(context=self.context, **kwargs)
        self.send([self.serializer.serialize(o) for o in object_list])

    def get_single(self, **kwargs):
        obj = self.get_object(**kwargs)
        self.send_single(obj, **kwargs)
        return obj

    def send_single(self, obj, **kwargs):
        self.serializer = self.serializer_class(context=self.context, instance=obj, **kwargs)
        self.send(self.serializer.serialize())

    def on_error(self, errors):
        self.send_error(errors)

    def create(self, **kwargs):
        kwargs = replace_original_with_data(kwargs)
        initials = self.get_initials('create', **kwargs)
        self.serializer = self.serializer_class(context=self.context, **kwargs)
        obj = self.serializer.deserialize(initials=initials, **kwargs)
        errors = self.serializer.is_valid(obj)
        if errors:
            self.on_error(errors)
            return

        obj.save()
        self.serializer.instance = obj
        self.created(obj)

    def created(self, obj):
        self.send(self.serializer.serialize(obj))

    def update(self, **kwargs):
        kwargs = replace_original_with_data(kwargs)
        initials = self.get_initials('update', **kwargs)
        obj = self.get_object(**kwargs)
        self.serializer = self.serializer_class(context=self.context, instance=obj, **kwargs)
        past_state = self.serializer.serialize()
        self.serializer.instance = self.serializer.deserialize(obj, initials=initials, **kwargs)
        errors = self.serializer.is_valid(self.serializer.instance)
        if errors:
            self.on_error(errors)
            return
        updated_data = self._get_changes(self.serializer.serialize(), past_state)
        self.serializer.instance.save()
        self.updated(self.serializer.instance, updated_data=updated_data, past_state=past_state)

    def updated(self, obj, **kwargs):
        self.send(kwargs.get('updated_data'))

    def delete(self, **kwargs):
        self.serializer = self.serializer_class(context=self.context, **kwargs)
        obj = self.get_object(**kwargs)
        self.deleted(obj)
        obj.delete()

    def deleted(self, obj):
        serialized_obj = self.serializer.serialize(obj)
        self.send(serialized_obj)


class BaseModelPublisherRouter(BaseModelRouter):
    include_related = []

    def publish_action(self, channels, data, action):
        publish_data = dict({'data': data})
        publish_data['action'] = action
        # publish_data['channel'] = channel
        self.publish(channels, publish_data)

    def created(self, obj):
        super(BaseModelPublisherRouter, self).updated(obj)
        base_channel = self.serializer_class.get_base_channel()
        all_model_channels = self.connection.pub_sub.get_channels(base_channel)
        channels = filter_channels_by_model(all_model_channels, obj)
        self.publish_action(channels, self.serializer.serialize(obj), PUBACTIONS.created)

    def updated(self, obj, **kwargs):
        super(BaseModelPublisherRouter, self).updated(obj, **kwargs)
        publish_model(
            obj,
            self.serializer_class(),
            self.connection.pub_sub,
            PUBACTIONS.updated, kwargs.get('past_state')
        )

    def deleted(self, obj, **kwargs):
        super(BaseModelPublisherRouter, self).deleted(obj, **kwargs)
        base_channel = self.serializer_class.get_base_channel()
        all_model_channels = self.connection.pub_sub.get_channels(base_channel)
        channels = filter_channels_by_model(all_model_channels, obj)
        data = dict(self.serializer.serialize(obj))
        data[self.serializer.id_field] = kwargs.get(self.serializer.id_field)
        self.publish_action(channels, data, PUBACTIONS.deleted)

    def subscribe(self, **kwargs):
        client_channel = kwargs.pop('channel')
        server_channels = make_channels(self.serializer_class, self.include_related, **self.get_subscription_context(**kwargs))
        self.send(
            data=self.serializer_class.get_object_map(self.include_related),
            channel_setup=self.make_channel_data(client_channel, server_channels)
        )
        self.connection.pub_sub.subscribe(server_channels, self.connection)

    def unsubscribe(self, **kwargs):
        client_channel = kwargs.pop('channel')
        server_channels = make_channels(self.serializer_class, self.include_related, **self.get_subscription_context(**kwargs))
        self.send(data='unsubscribed', channel_setup=self.make_channel_data(client_channel, server_channels))
        self.connection.pub_sub.unsubscribe(server_channels, self.connection)


def register(route):
    if route in registered_handlers:
        return
    route_name = route.get_name()
    registered_handlers[route_name] = route


def get_route_handler(name):
    return registered_handlers[name]
