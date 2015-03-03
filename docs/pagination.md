# Pagination #


## Route handler ##

Adding pagination is simple.

Set `paginate_by=<num>` in your route handler.

```python
class FooRoute(ModelRouter):
    (...)
    paginate_by=10
```

## Javascript ##

Set `_page=<num>` when calling get_list

```javascript
(...)
var args = {'_page': 1};
swampDragon.get_list(route, args, callbackName)
```

## Angular ##

```javascript
var page = 1;
dataService.getPagedList(route, {}, page).then(function (response) {
    // handle data
});
```
