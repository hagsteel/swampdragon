# Pagination #

To enable pagination simply set the `paginate_by` property on your router.

```python
from swampdragon.route_handler import ModelRouter


class FooRouter(ModelRouter):
    paginate_by = 10

    ...
```

> This only applies to `ModelRouter` and `ModelPublisherRouter`


## Javascript ##

Set `_page=<num>` when calling get_list

```javascript
...
var args = {'_page': 1};
swampDragon.get_list(route, args, callbackName)
```


## Angular ##

```javascript
var page = 1;
$dragon.data.getPagedList(route, {}, page).then(function (response) {
    // handle data
});
```
