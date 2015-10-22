from .pubsub_providers.publisher_factory import get_publisher
from .paginator import Paginator
from .pubsub_providers.base_provider import PUBACTIONS
from .message_format import format_message
from .pubsub_providers.model_channel_builder import make_channels, filter_channels_by_model, filter_channels_by_dict
from .serializers.validation import ModelValidationError

SUCCESS = 'success'
ERROR = 'error'
LOGIN_REQUIRED = 'login_required'

CHANNEL_DATA_SUBSCRIBE = 'subscribe'
CHANNEL_DATA_UNSUBSCRIBE = 'unsubscribe'

registered_handlers = {}

publisher = get_publisher()


class UnexpectedVerbException(Exception):
    pass


class RouteException(Exception):
    pass


class BaseRouter(object):
    valid_verbs = ['get_list', 'get_single', 'create', 'update', 'delete', 'subscribe', 'unsubscribe']
    exclude_verbs = []
    serializer = None
    route_name = None
    permission_classes = []

    def __init__(self, connection, request=None, **kwargs):
        self.connection = connection
        self.context = dict()

    def make_channel_data(self, client_channel, server_channels, action):
        return {'local_channel': client_channel, 'remote_channels': server_channels, 'action': action}

    @classmethod
    def get_name(cls):
        route_name = getattr(cls, 'route_name')
        if not route_name:
            raise Exception('\n------\n{} has no name.\nSet the route_name property\n------\n'.format(cls.__name__))
        return route_name

    def handle(self, data):
        verb = data['verb']
        kwargs = data.get('args') or {}
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
        '''
        Additional data to be sent to the client with each `send` call
        from the router
        '''
        return {}

    def _update_client_context(self, data):
        if not data:
            return
        if 'client_context' not in self.context:
            self.context['client_context'] = {}
        self.context['client_context'].update(data)

    def get_list(self, **kwargs):
        raise NotImplementedError('get_list is not implemented')

    def get_single(self, **kwargs):
        raise NotImplementedError('get_single is not implemented')

    def create(self, **kwargs):
        raise NotImplementedError('create is not implemented')

    def update(self, **kwargs):
        raise NotImplementedError('update is not implemented')

    def delete(self, **kwargs):
        raise NotImplementedError('delete is not implemented')

    def send(self, data, channel_setup=None, **kwargs):
        self.context['state'] = SUCCESS
        if 'verb' in self.context:
            client_context = self.get_client_context(self.context['verb'], **kwargs)
            self._update_client_context(client_context)

        message = format_message(data=data, context=self.context, channel_setup=channel_setup)
        self.connection.send(message)

    def send_error(self, data, channel_setup=None):
        self.context['state'] = ERROR
        self.connection.send(format_message(data=data, context=self.context, channel_setup=channel_setup))

    def send_login_required(self, channel_setup=None):
        self.context['state'] = LOGIN_REQUIRED
        self.connection.send(format_message(data=None, context=self.context, channel_setup=channel_setup))

    def get_subscription_channels(self, **kwargs):
        raise NotImplementedError()

    def subscribe(self, **kwargs):
        client_channel = kwargs.pop('channel')
        server_channels = self.get_subscription_channels(**kwargs)
        self.send(
            data='subscribed',
            channel_setup=self.make_channel_data(client_channel, server_channels, CHANNEL_DATA_SUBSCRIBE),
            **kwargs)
        self.connection.pub_sub.subscribe(server_channels, self.connection)

    def unsubscribe(self, **kwargs):
        client_channel = kwargs.pop('channel')
        server_channels = self.get_subscription_channels(**kwargs)
        self.send(
            data='unsubscribed',
            channel_setup=self.make_channel_data(client_channel, server_channels, CHANNEL_DATA_UNSUBSCRIBE),
            **kwargs
        )
        self.connection.pub_sub.unsubscribe(server_channels, self.connection)

    def publish(self, channels, publish_data):
        for channel in channels:
            publish_data['channel'] = channel
            self.connection.pub_sub.publish(channel, publish_data)


class BaseModelRouter(BaseRouter):
    model = None
    serializer_class = None
    instance = None
    include_related = []
    paginate_by = None
    _query_set = None
    _obj = None

    def _get_changed_fields(self, current_state, past_state):
        '''
        Compare the previous data with the current data
        to get only the changed fields
        '''
        changed_fields = []
        for o in current_state:
            if past_state[o] != current_state[o]:
                changed_fields.append(o)
        return changed_fields

    def _get_object(self, **kwargs):
        if self._obj:
            return self._obj
        self._obj = self.get_object(**kwargs)
        return self._obj

    def _get_query_set(self, **kwargs):
        if self._query_set:
            return self._query_set
        self._query_set = self.get_query_set(**kwargs)
        return self._query_set

    def get_list(self, **kwargs):
        obj_list = self._get_query_set(**kwargs)
        if self.paginate_by:
            page_num = self.context.get('page', 1)
            page = Paginator(obj_list, self.paginate_by).page(page_num)
            self._update_client_context({'page': page.serialize()})
            obj_list = page.object_list

        self.send_list(obj_list, **kwargs)
        return obj_list

    def get_initial(self, verb, **kwargs):
        return dict()

    def get_subscription_contexts(self, **kwargs):
        return dict(kwargs)

    def send_list(self, object_list, **kwargs):
        self.send([self.serializer_class(instance=o).serialize() for o in object_list], **kwargs)

    def get_single(self, **kwargs):
        obj = self._get_object(**kwargs)
        self.send_single(obj, **kwargs)
        return obj

    def send_single(self, obj, **kwargs):
        self.serializer = self.serializer_class(instance=obj)
        self.send(self.serializer.serialize(), **kwargs)

    def on_error(self, errors):
        self.send_error(errors)

    def create(self, **kwargs):
        initial = self.get_initial('create', **kwargs)
        self.serializer = self.serializer_class(data=kwargs, initial=initial)
        try:
            obj = self.serializer.save()
        except ModelValidationError as error:
            self.on_error(error.get_error_dict())
            return

        obj.save()
        self.created(obj, **kwargs)

    def created(self, obj, **kwargs):
        self.send(self.serializer.serialize())

    def update(self, **kwargs):
        initial = self.get_initial('update', **kwargs)
        obj = self._get_object(**kwargs)
        self.serializer = self.serializer_class(instance=obj, data=kwargs, initial=initial)
        past_state = self.serializer.serialize()
        try:
            self.serializer.save()
        except ModelValidationError as error:
            errors = error.get_error_dict()
            self.on_error(errors)
            return
        updated_fields = self._get_changed_fields(self.serializer.serialize(), past_state)

        self.updated(self.serializer.instance, updated_fields=updated_fields, past_state=past_state)

    def updated(self, obj, **kwargs):
        updated_fields = kwargs.get('updated_fields')
        self.send(self.serializer.serialize(fields=updated_fields), **kwargs)

    def delete(self, **kwargs):
        obj = self._get_object(**kwargs)
        self.serializer = self.serializer_class(instance=obj, data=kwargs)
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
        channel_setup = self.make_channel_data(client_channel, server_channels, CHANNEL_DATA_SUBSCRIBE)
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
            channel_setup=self.make_channel_data(client_channel, server_channels, CHANNEL_DATA_UNSUBSCRIBE),
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
        all_model_channels = publisher.get_channels(base_channel)
        channels = filter_channels_by_model(all_model_channels, obj)
        self.publish_action(channels, self.serializer_class(instance=obj).serialize(), PUBACTIONS.created)

    def updated(self, obj, **kwargs):
        super(BaseModelPublisherRouter, self).updated(obj, **kwargs)
        base_channel = self.serializer_class.get_base_channel()
        all_model_channels = publisher.get_channels(base_channel)
        channels = filter_channels_by_model(all_model_channels, obj)
        updated_fields = kwargs.get('updated_fields')
        self.publish_action(channels, self.serializer.serialize(fields=updated_fields), PUBACTIONS.updated)
        past_state = kwargs.get('past_state')
        if past_state:
            previous_channels = filter_channels_by_dict(all_model_channels, past_state)
            delete_from_channels = set(previous_channels) - set(channels)
            self.publish_action(delete_from_channels, past_state, PUBACTIONS.deleted)

    def deleted(self, obj, obj_id, **kwargs):
        super(BaseModelPublisherRouter, self).deleted(obj, obj_id, **kwargs)
        base_channel = self.serializer_class.get_base_channel()
        all_model_channels = publisher.get_channels(base_channel)
        channels = filter_channels_by_model(all_model_channels, obj)
        data = self.serializer.serialize()
        self.publish_action(channels, data, PUBACTIONS.deleted)


class ModelRouter(BaseModelRouter):
    pass


class ModelPubRouter(BaseModelPublisherRouter):
    pass


def register(route):
    if route.get_name() in registered_handlers:
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
    if name not in registered_handlers:
        raise RouteException('No route named "{}"'.format(name))
    return registered_handlers[name]
