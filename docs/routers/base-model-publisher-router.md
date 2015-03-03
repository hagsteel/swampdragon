# ModelPubRouter #

The `ModelPubRouter` is similar to `ModelRouter` with one exceptions:
the `ModelPubRouter` will publish data when a CRUD function is invoked on the router.

This router is a good option when self-publishing models are not used.
Since a self-publishing model will publish it self when it's changed, this could result in duplicate updates.

If a model shouldn't be published unless certain criteria is met, it's better to use the ModelPublisherRouter.

Override the `created`, `updated` and/or `deleted` function to handle the data being published.

The benefits of using the `ModelPubRouter` instead of making every model a self-publishing model is
to have control over the publishing process.

In the following scenario we only publish models that have a specific rating:

```python
from swampdragon import route_handler
from swampdragon.route_handler import ModelPubRouter


class FooRouter(ModelPubRouter):
    model = Foo
    serializer_class = FooSerializer

    def updated(self, obj, **kwargs):
        if obj.rating < 3:
            # We don't publish this model because the rating is too low.
            return
        super().updated(obj, **kwargs)

    def created(self, obj, **kwargs):
        # We don't want to publish this model when it's created,
        # because the rating is too low.
        return

route_handler.register(FooRouter)
```

If the **Foo** `model` was simply a self publishing model it would have published the update.
This way we can ensure that only **Foo** instances with a rating over 3 is posted
