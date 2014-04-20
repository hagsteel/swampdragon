Swamp Dragon
============

# UNDER DEVELOPMENT

Swamp Dragon is a pub/sub solution running on top of Tornado, and is compatible with Django models.
It allows data to be published to channels via routers and does all the heavy lifting.


# Important
**Note**: As Django models are blocking, long queries will prevent other requests to come through.

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
*  Write documentation
*  Add instructions for swampDragon.call = function(verb, route, channel, args, callbackName)
*  Add instructions on self publishing models
*  term_match_check: make sure compared values are of the same type
*  Filter case sensitivity


# Routers
Routers routes the messages to the right handler.


## Route permissions

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


