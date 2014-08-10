from .paginator import Paginator
from .sessions.sessions import get_session_store
from .pubsub_providers.base_provider import PUBACTIONS
from .message_format import format_message
from .pubsub_providers.model_channel_builder import make_channels, filter_channels_by_model
from .pubsub_providers.model_publisher import publish_model
from .serializers.validation import ModelValidationError


registered_handlers = {}


class UnexpectedVerbException(Exception):
    pass


class BaseRouter(object):
    valid_verbs = ['get_list', 'get_single', 'create', 'update', 'delete', 'subscribe', 'unsubscribe']
    exclude_verbs = []
    serializer_class = None
    serializer = None
    route_name = None
    permission_classes = []
    session_store = get_session_store()

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
        self.context['client_callback_name'] = client_callback_name
        self.context['verb'] = verb
        if '_page' in kwargs:
            self.context['page'] = kwargs.pop('_page')

        if verb in self.valid_verbs:
            m = getattr(self, verb)
            if self.permission_classes:
                for permission in self.permission_classes:
                    if not permission.test_permission(self, verb, **kwargs):
                        permission.permission_failed(self)
                        return
            m(**kwargs)
        else:
            if verb not in self.exclude_verbs:
                raise UnexpectedVerbException('\n------\nUnexpected verb: {}\n------'.format(verb))

    def get_client_context(self, verb, **kwargs):
        return {}

    def _update_client_context(self, data):
        if not data:
            return
        if 'client_context' not in self.context:
            self.context['client_context'] = {}
        self.context['client_context'].update(data)

    def get_list(self, **kwargs):
        raise NotImplemented('get_list is not implemented')

    def got_list(self, **kwargs):
        raise NotImplemented('got_list is not implemented')

    def get_single(self, **kwargs):
        raise NotImplemented('get_single is not implemented')

    def create(self, **kwargs):
        raise NotImplemented('create is not implemented')

    def update(self, **kwargs):
        raise NotImplemented('update is not implemented')

    def action_failed(self, **kwargs):
        self.send_error({self.context['verb']: 'failed'})

    def delete(self, **kwargs):
        raise NotImplemented('delete is not implemented')

    def get_initials(self, verb, **kwargs):
        return dict()

    def send(self, data, channel_setup=None, **kwargs):
        self.context['state'] = 'success'

        if 'verb' in self.context:
            client_context = self.get_client_context(self.context['verb'], **kwargs)
            self._update_client_context(client_context)

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
        self.send(
            data='subscribed',
            channel_setup=self.make_channel_data(client_channel, server_channels),
            **kwargs)
        self.connection.pub_sub.subscribe(server_channels, self.connection)

    def unsubscribe(self, **kwargs):
        client_channel = kwargs.pop('channel')
        server_channels = self.get_subscription_channels(**kwargs)
        self.send(
            data='unsubscribed',
            channel_setup=self.make_channel_data(client_channel, server_channels),
            **kwargs
        )
        self.connection.pub_sub.unsubscribe(server_channels, self.connection)

    def publish(self, channels, publish_data):
        for channel in channels:
            publish_data['channel'] = channel
            self.connection.pub_sub.publish(channel, publish_data)

    def get_subscription_contexts(self, **kwargs):
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
    include_related = []
    paginate_by = None
    _query_set = None
    _obj = None

    def _get_changes(self, current_state, past_state):
        changed_state = {}

        for o in current_state:
            if past_state[o] != current_state[o]:
                changed_state[o] = current_state[o]
        if self.serializer.opts.id_field not in changed_state:
            changed_state['id'] = current_state['id']
        return changed_state

    def _get_query_set(self, **kwargs):
        if self._query_set:
            return self._query_set
        self._query_set = self.get_query_set(**kwargs)
        return self._query_set

    def _get_object(self, **kwargs):
        if self._obj:
            return self._obj
        self._obj = self.get_object(**kwargs)
        return self._obj

    def get_list(self, **kwargs):
        obj_list = self.get_query_set(**kwargs)
        if self.paginate_by and self.context['page']:
            page = Paginator(obj_list, self.paginate_by).page(self.context['page'])
            self._update_client_context({'page': page.serialize()})
            obj_list = page.object_list

        self.send_list(obj_list, **kwargs)
        return obj_list

    def send_list(self, object_list, **kwargs):
        self.send([self.serializer_class(instance=o).serialize() for o in object_list], **kwargs)

    def get_single(self, **kwargs):
        obj = self.get_object(**kwargs)
        if not obj:
            return self.action_failed(**kwargs)
        self.send_single(obj, **kwargs)
        return obj

    def send_single(self, obj, **kwargs):
        self.serializer = self.serializer_class(instance=obj)
        self.send(self.serializer.serialize(), **kwargs)

    def on_error(self, errors):
        self.send_error(errors)

    def create(self, **kwargs):
        kwargs = replace_original_with_data(kwargs)
        initials = self.get_initials('create', **kwargs)
        # self.serializer = self.serializer_class(context=self.context, **kwargs)
        self.serializer = self.serializer_class(data=kwargs, initial=initials)
        try:
            obj = self.serializer.save()
        except ModelValidationError as error:
            self.on_error(error.get_error_dict())
            return

        obj.save()
        self.created(obj, **kwargs)

    def created(self, obj, **kwargs):
        if not self.serializer:
            self.serializer = self.serializer_class(obj)
        self.send(self.serializer.serialize())

    def update(self, **kwargs):
        kwargs = replace_original_with_data(kwargs)
        initial = self.get_initials('update', **kwargs)
        obj = self.get_object(**kwargs)
        if not obj:
            return self.action_failed(**kwargs)
        self.serializer = self.serializer_class(instance=obj, data=kwargs, initial=initial)
        past_state = self.serializer.serialize()
        try:
            self.serializer.save()
        except ModelValidationError as error:
            errors = error.get_error_dict()
            self.on_error(errors)
            return
        updated_data = self._get_changes(self.serializer.serialize(), past_state)
        self.updated(self.serializer.instance, updated_data=updated_data, past_state=past_state)

    def updated(self, obj, **kwargs):
        self.send(kwargs.get('updated_data'), **kwargs)

    def delete(self, **kwargs):
        obj = self.get_object(**kwargs)
        self.serializer = self.serializer_class(instance=obj, data=kwargs)
        if not obj:
            return self.action_failed(**kwargs)
        obj_id = obj.pk
        self.deleted(obj, obj_id, **kwargs)
        obj.delete()

    def deleted(self, obj, obj_id, **kwargs):
        serialized_obj = self.serializer.serialize()
        self.send(serialized_obj, **kwargs)

    def subscribe(self, **kwargs):
        client_channel = kwargs.pop('channel')
        server_channels = make_channels(self.serializer_class, self.include_related, self.get_subscription_contexts(**kwargs))
        data = self.serializer_class.get_object_map(self.include_related)
        channel_setup = self.make_channel_data(client_channel, server_channels)
        self.send(
            data=data,
            channel_setup=channel_setup,
            **kwargs
        )
        self.connection.pub_sub.subscribe(server_channels, self.connection)

    def unsubscribe(self, **kwargs):
        client_channel = kwargs.pop('channel')
        server_channels = make_channels(self.serializer_class, self.include_related, self.get_subscription_contexts(**kwargs))
        self.send(
            data='unsubscribed',
            channel_setup=self.make_channel_data(client_channel, server_channels),
            **kwargs)
        self.connection.pub_sub.unsubscribe(server_channels, self.connection)


class BaseModelPublisherRouter(BaseModelRouter):
    def publish_action(self, channels, data, action):
        publish_data = dict({'data': data})
        publish_data['action'] = action
        self.publish(channels, publish_data)

    def created(self, obj, **kwargs):
        super(BaseModelPublisherRouter, self).created(obj)
        base_channel = self.serializer_class.get_base_channel()
        all_model_channels = self.connection.pub_sub.get_channels(base_channel)
        channels = filter_channels_by_model(all_model_channels, obj)
        self.publish_action(channels, self.serializer_class(instance=obj).serialize(), PUBACTIONS.created)

    def updated(self, obj, **kwargs):
        super(BaseModelPublisherRouter, self).updated(obj, **kwargs)
        publish_model(
            obj,
            self.serializer_class(instance=obj),
            self.connection.pub_sub,
            PUBACTIONS.updated, kwargs.get('past_state')
        )

    def deleted(self, obj, obj_id, **kwargs):
        super(BaseModelPublisherRouter, self).deleted(obj, obj_id, **kwargs)
        base_channel = self.serializer_class.get_base_channel()
        all_model_channels = self.connection.pub_sub.get_channels(base_channel)
        channels = filter_channels_by_model(all_model_channels, obj)
        data = self.serializer.serialize()
        data[self.serializer.opts.id_field] = obj_id
        self.publish_action(channels, data, PUBACTIONS.deleted)


def register(route):
    if route in registered_handlers:
        return
    if issubclass(route, BaseModelRouter) or issubclass(route, BaseModelPublisherRouter):
        if 'get_single' in route.valid_verbs and 'get_single' not in route.exclude_verbs:
            if not hasattr(route, 'get_object'):
                raise Exception('\n-----------\nget_object needs to be implemented if get_single is available ({})\n-----------\n'.format(route.__name__))
        if 'get_list' in route.valid_verbs and 'get_list' not in route.exclude_verbs:
            if not hasattr(route, 'get_query_set'):
                raise Exception('\n-----------\nget_query_set needs to be implemented if get_list is available ({})\n-----------\n'.format(route.__name__))
    route_name = route.get_name()
    registered_handlers[route_name] = route


def get_route_handler(name):
    return registered_handlers[name]
