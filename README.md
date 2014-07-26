Swamp Dragon
============

# UNDER DEVELOPMENT

Swamp Dragon is a pub/sub solution running on top of Tornado, and is compatible with Django models.
It allows data to be published to channels via routers and does all the heavy lifting.


# Important
**Note**: As Django models are blocking, long queries will prevent other requests from coming through.

**Note**: Currently it's heavily tied to Django

**Note**: All serializers needs to reside in serializers.py

**Note**: Angular doesn't include a checkbox ng-model unless a value is set.
This means adding a checkbox with ng-model="mymodel.flag" will not be included when submitting data,
unless the checkbox is ticked or mymodel is initiated ```scope.mymodel = { flag=false };```

**Note**: Calling update on a queryset won't work on self publishing models.
i.e ```MyModel.objects.all().update(foo=bar)``` won't trigger a publishing action


#TODO
*  Dirty fields in the front end (don't update forms)
*  Auto discover routes returns URLs and needs to be renamed
*  Add instructions for swampDragon.call = function(verb, route, channel, args, callbackName)
*  Add instructions on self publishing models
*  term_match_check: make sure compared values are of the same type
*  Filter case sensitivity


# Tornado 4.0
If you experience ```Error during WebSocket handshake: Unexpected response code: 403``` you might have to run 
the latest dev version of sockjs-tornado.

```pip uninstall sockjs-tornado```
```pip install -e git+https://github.com/mrjoes/sockjs-tornado.git#egg=sockjs-tornado```

This should solve the error message.


# Routers
Routers routes the messages to the right handler.


## Route permissions

```LoginRequired``` is a built in permission.

Route permissions takes a list of permissions

    class FooRoute(BaseRoute):
        model = FooModel
        serializer_class = FooModelSerializer
        route_name = 'foo'
        permission_classes = [LoginRequired(), CustomPermission()]

You can create your own custom permissions:

    class CustomPermission(RoutePermission):
        def test_permission(self, handler, verb, **kwargs):
            if verb == 'update':
                return False
            return True

        def permission_failed(self, handler):
            handler.send_error(data={'message': 'update is not allowed'})

This permission sends an error in case anyone is trying to call the ```update``` verb.
** Note ** This permission is an example, if updates weren't allowed, then the ```valid_verbs```
would be a more suitable option.


## Subscription
Subscribe a connection to one or more channel.
For model subscriptions, the router should inherit from ```BaseModelPublisherRouter```.


### BaseModelPublisherRouter
There are a couple of key functions in the ```BaseModelPublisherRouter```. 


#### ```get_subscription_contexts```
The subscription context should return a dictionary containing keys and values to filter on.
i.e

    def get_subscription_contexts(self, **kwargs):
        return {
            'name__contains': 'foo',
            'owner_id': self.connection.user.pk
        }
    
In the above code, the router would publish data where the data has a name that contains the word foo, and the 
owner id is a users primary key.


#### ```publish_action```

The ```publish_action``` takes three arguments: ```channels```, ```data```, ```action ```.
The channels are the channels to publish to, data is a dictionary containing the data to publish, and the action
is either ```PUBACTIONS.created```, ```PUBACTIONS.updated``` or ```PUBACTIONS.deleted```.
The action is required for the data mapper in the front end, to know how to handle the incoming data.

If a call to the router is any of the default actions of the router (```create```, ```updated``` or ```delete```) there is no need
to call ```publish_action``` as these functions will handle it.

In most cases the only reason to call publish_action is when a specific verb has been defined.


## Pagination


### Route handler
Adding pagination is easy.
Set ```paginate_by=<num>``` in your route handler.

    class FooRoute(BaseModelRouter):
        ...
        paginate_by=10


### Javascript
Set ```_page=<num>``` when calling get_list
var args = {'_page': 1};
swampDragon.get_list(route, args, callbackName)


#### Angular

        var page = 1;
        dataService.getPagedList(route, {}, page).then(function (response) {
            // handle data
        });


# Sessions

Storing values for a period of time is done in the session store.
The default session store is RedisSessionStore, which reads and writes to Redis

To create your own session store, inherit from ```BaseSessionStore```.
Assign the store by setting ```DRAGON_SESSION_STORE``` in your settings file.

i.e DRAGON_SESSION_STORE = 'app.session_store.FooSessionStore'

You have to implement the expiration procedure manually.

Implementing your own session store requires two functions:

class FooSessionStore(object):
    def save(self, key, val):
        ...

    def get(self, key):
        ...

Currently the keys are plain UUIDs. If you want to manufacture your own session keys, override ```generate_key```.

## Session refresh

Currently there is no built in way to refresh the expiration of a session.
You manually have to handle keeping the session alive.

One way of doing this would be to ues the heartbeat functionality

In this example we create a data connection.
When the connection is open, we start a periodic callback (import ```from tornado.ioloop import PeriodicCallback```).
We set the callback to occur every 10 minutes, where we send a heartbeat message to the client.
The client is expected to send a heartbeat message back, containing the session key.
If the session key is available: call ```refresh_key_timeout``` on the session store.


    class DataConnection(SubscriberConnection):
        def on_open(self, request):
            super(DataConnection, self).on_open(request)
            self.session_store = get_session_store()
            self.start_heartbeat()
            self.periodic_callback = None

        def on_close(self):
            super(DataConnection, self).on_close()
            self.periodic_callback.stop()

        def start_heartbeat(self):
            ms_minute = 1000 * 60
            self.periodic_callback = PeriodicCallback(self.on_heartbeat, ms_minute * 10)
            self.periodic_callback.start()

        def on_heartbeat(self):
            self.send({'heartbeat': 'tick'})

        def on_message(self, data):
            if 'heartbeat' in data:
                try:
                    json_data = json.loads(data)
                    self.session_store.refresh_key_timeout(json_data['session'])
                    return
                except:
                    pass
            super(DataConnection, self).on_message(data)


When instantiating the SwampDragon javascript object, there is an optional callback
call ```onheartbeat```, that can be used to react on a heartbeat message and send the session key
to the server.

Note: the angular service will issue ```$rootScope.$broadcast('heartbeat');``` on this event.


# File upload

File upload is currently only supported by:
*  Chrome 7+
*  Firefox 4+
*  IE 10+
*  Opera 12+
*  Safari 5+

Reference /static/swampdragon/js/fileupload.js
If you are using AngularJS make sure you include swampdragon/js/angular/directives.js.

## Angular
When declaring your app, include SDFileUploader.

    var FooApp = angular.module('FooApp', [
        'SDFileUploader',
        ...
    ]);

In your angular template assign the ```sd-file-uploader``` directive on your file input,
and set your route path as the attribute.

    <input type="file" sd-file-uploader="/accounts/" ng-model="profile.photo">

