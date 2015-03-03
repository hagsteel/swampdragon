# ModelRouter

The base model router is used to create, read, update and delete Django models.

```python

class FooModelRouter(ModelRouter):
    route_name = 'foo-model'
    serializer_class = FooModelSerializer
    model = FooModel

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['pk'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()


route_handler.register(FooModelRouter)
```

It is also the recommended router for self-publishing models as it won't publish when ```updated``` is invoked.

Both the ```ModelRouter``` and the ```ModelPublisherRouter``` requires a model and serializer class.


## get_object and get_query_set

The ```get_object``` and ```get_query_set``` function is analogous to Django's class based views.

By default a router provides verbs for ```get_single``` and ```get_list```. Rather than overriding these function,
simply define get_object or get_query_set.

If a router is either a ```ModelRouter``` or a ```ModelPublisherRouter``` and all the default verbs are
available, SwampDragon will raise an exception when you try to start the server if get_single and get_query_set are
both missing.

This is to ensure that no data will be exposed without being handled by the programmer first.