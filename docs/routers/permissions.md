# Permissions #

There are two types of permissions:

*  verb (function) based permission
*  class based permission


## Login required ##

The `login_required` requires a `user` property on the connection.

This means the permission will not work unless you use a custom connection with a user property.
The simplest way is to use [swampdragon-auth](https://github.com/jonashagstedt/swampdragon-auth), or create your own
connection, extending `DjangoSubscriberConnection` with a user property.

It can be used by either specifying the `permission_classes` on the router:

```python
from swampdragon.route_handler import ModelRouter


class FooRouter(ModelRouter):
    ...
    permission_classes = [LoginRequired()]
```

or setting it directly as `decorator` on a a verb:

```python
from swampdragon.route_handler import ModelRouter


class FooRouter(ModelRouter):
    ...
    @login_required
    foo_verb(self, **kwargs):
        ...
```


## Custom permission ##

Creating a custom permission is done by extending `RoutePermission`.

Two functions are required:

```python
def test_permission(self, handler, verb, **kwargs):
    ...

def permission_failed(self, handler):
    ...
```

`test_permission` takes the route handler, and the current verb it's testing.
It should return a boolean value of either True or False.

If the permission check fails, the router will call `permission_failed`.
