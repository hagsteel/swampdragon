# BaseRouter #

The base router is a good place to start when building anything that isn't directly related to a model or a serializer.

A router consists of a series of verbs, which are user defined functions.

A function should finish by calling either `send` or `send_error`.


```python
from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter


class FooRouter(BaseRouter):
    route_name = 'foo'
    valid_verbs = ['get_date']

    def get_date(self, **kwargs):
        self.send({'current_date': str(datetime.now())})


route_handler.register(FooRouter)
```
