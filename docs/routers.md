# Routers

Routers handles the messages sent to the server from the client.

There are 3 different types of base routers:

+  BaseRouter
+  BaseModelRouter
+  BaseModelPublisherRouter

------


## Selecting a router

The ```BaseRouter``` is ideal for scenarios when you are not dealing with models.

The ```BaseModelRouter``` is suited for scenarios when you want to read / write models.

The ```BaseModelPublisherRouter``` is similar to the BaseModelRouter, with the exception that it handles 
subscriptions. 


## BaseRouter

The base router is a good place to start when building anything that isn't directly related to a model or a serializer.

A router consists of verbs, that should end with either ```send``` or ```send_error```.

To specify the valid verbs for a router, set the property ```valid_verbs```.

The default setup for valid verbs is: ```valid_verbs = ['get_list', 'get_single', 'create', 'update', 'delete', 'subscribe', 'unsubscribe']```.

For clients to be able to call your router, you need to implement a valid verb, a route name and finally register the router.

    class FooRouter(BaseRouter):
        route_name = 'foo'
        valid_verbs = ['get_date']
    
        def get_date(self, **kwargs):
            self.send({'current_date': str(datetime.now())})
                    
            
    route_handler.register(FooRouter)
    

The ```send``` function only accepts dicts (containing json serializable values) or strings.


## BaseModelRouter

The base model router is used to create, read, update and delete Django models.

    class FooModelRouter(BaseModelRouter):
        route_name = 'foo-model'
        serializer_class = FooModelSerializer
        model = FooModel
    
        def get_object(self, **kwargs):
            return self.model.objects.get(pk=kwargs['pk'])
    
        def get_query_set(self, **kwargs):
            return self.model.objects.all()
    
    
    route_handler.register(FooModelRouter)

In the above example, since all verbs are valid by default, a user could get a single instance of a FooModel, 
all the models, create, update and delete a model.

The BaseModelRouter handles creating and updating of models with help of the serializer.
A call to the routers ```create``` function tries to create an instance of the model. 
If there is a validation error, ```on_error``` will be called (which simply calls ```send_error(errors)```).

In case of any functionality before sending a validation error to the client, override ```def on_error(errors)```, where
errors is simply a dict, and finally call ```self.send_error(errors)```.

    ...
    def on_error(errors):
        # Perform any desired logic here
        self.send_error(errors)

Once the create function has successfully created an instance of the routers model, ```created``` will be called.
Any functionality after creating an instance of a model can be executed by overriding the ```created``` function

    ...
    def created(self, obj, **kwargs):
        # Perform any desired operation here
        self.send(self.serializer.serialize(obj))
        
The same logic applies to ```create``` and ```created```.


# BaseModelPublisherRouter

This router handles subscriptions to various channels, allowing data to be pushed to the connected clients.

To determine which clients receive the published data, the ```get_subscription_contexts``` should be implemented.

The following example publishes data to all clients subscribing to the model, where the text contains 'foo' and the 
number value is less than 10. 

    ...
    def get_subscription_contexts(self, **kwargs):
        return {
            'text__contains': 'foo',
            'number__lt': 10
        }
   
In case of data that is user specific, the ```get_subscription_contexts``` could be implemented as follow:

    ...
    def get_subscription_contexts(self, **kwargs):
        return {user_id: self.connection.get_user().pk}
        
Data matching that specific users id would only be sent to that user.

Unlike the ```BaseModelRouter``` the ```BaseModelPublisherRouter``` have more advanced created / updated
functionality:

Once a model is updated, create or deleted, the BaseModelPublisherRouter will publish the updates to all
channels matching the instances field values.