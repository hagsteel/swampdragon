# Routers

Routers handle messages sent to and from the server and the client.

Routers fills a similar purpose to views in Django.

There are 3 different types of base routers

+  [BaseRouter](/documentation/routers-base-router/)
+  [ModelRouter](/documentation/routers-base-model-router/)
+  [ModelPublisherRouter](/documentation/routers-base-model-publisher-router/)

For a general guide on choosing your base router, see [Choosing a router](/documentation/choosing-a-router/) 


## Overview 

Every router requires a route name that can be used by the client to call the router.

    class FooRouter(...):
        route_name = 'foo-router'
        

Each router needs to be registered with the router handler

    class FooRouter(...):
        ...

    route_handler.register(FooRouter)

Routers should reside in routers.py, inside your app: ```myapp/routers.py``` to be able to be discovered by SwampDragon.


## Verbs

Verbs are paths that routers will react to. 

By default a router have the following verb setup

    valid_verbs = [
        'get_list', 'get_single', 'create', 'update', 'delete', 'subscribe', 'unsubscribe'
    ]
    
You can easily add your own verbs

    class FooRouter(BaseRouter):
        valid_verbs = BaseRouter.valid_verbs + ['say_hello']
        
        def say_hello(self, **kwargs):
            ...
        

In cases where you only want your own custom verbs, simply specify your verbs in ```valid_verbs```

    class BarRouter(BaseRouter):
        valid_verbs = ['my_verb', 'my_other_verb']
        
        def my_verb(**kwargs):
            ...
        
        def my_other_verb(**kwargs):
            ...

If a function isn't listed in valid_verbs any attempt to call the router with that verb will raise an ```InvalidVerbException```.


## Sending data

While verbs allow you to receive data, ```send``` is used to send data to the client.

    class FooRouter(BaseRouter):
        valid_verbs = ['what_time_is_it']
        
        def say_hello(self, **kwargs):
            self.send({'message': 'hello'})
            
Note that ```send``` should be called with a dictionary (and send only submits data to the client calling the verb, to publish see the ```publish``` function).


## Subscribing to a channel

One of the benefits with SwampDragon is being able to publish data to channels.

This is where ```get_subscription_contexts``` becomes relevant.

    class BazRouter(ModelRouter):
        ...
        
        def get_subscription_contexts(self, **kwargs):
            return {'foo__is_published': True, foo__bar__title__contains=kwargs['title']}
            
The following router would allow a user to subscribe to all published foo models where the title contains whatever title the user submitted.

Note that ```get_subscription_contexts``` only works with ModelRouter and ModelPublisherRouter as they are the only model based routers.

The following works with ```get_subscription_contexts```:

*  contains - contains a word
*  lt - less than
*  lte - less than or equal to 
*  gt - greater than
*  gte - greater than or equal to
*  eq - equal to 
*  in - value in list


For ```BaseRouter``` use ```get_subscription_channels``` (note that neither base model router 
calls get_subscription_channels)

    class FooRouter(BaseRouter):
        ...
        
        def get_subscription_channels(**kwargs):
            if 'group_a' in kwargs:
                return ['group_a']
            if 'group_b' in kwargs:
                return ['group_b']
            return ['group_a', 'group_b']
            

This is useful in scenarios where you would make, for instance, a chat with multiple rooms, or you want to post data from different sources.


## Subscribing to models


When subscribing to a ModelRouter it will, by default, subscribe to all changes to that model.
Use the ```get_subscription_context``` to filter the models.

Example: The following example would only publish changes to a model where the value is less than 100. 

    class FooModelRouter(ModelRouter):
        ...
        def get_subscription_context(self, **kwargs):
            return {value__lt: 100}
            


To subscribe to a model including changes to related models use ```include_related```.


    class FooModelRouter(ModelRouter):
        model = Foo
        serializer = FooSerializer
        include_related = [BarSerializer, BazSerializer]
        ...

Any changes to a Bar model will publish to the same channel as the Foo router.

## Sending errors

Each router have a function for sending errors.

    class FooRouter(BaseRouter):
        ...
        
        def create(self, **kwargs):
            if not 'name' in kwargs:
                self.send_error({'name': 'the name is required'})
            ...
            
Errors generally consist of a dictionary {name_of_property or source: error message(s)}