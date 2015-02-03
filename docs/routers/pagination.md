# Pagination

To enable pagination simply set the ```paginate_by``` property on your router.
    
    class FooRouter(ModelRouter):
        paginate_by = 10
        
        ...

This only applies to ```ModelRouter``` and ```ModelPublisherRouter```


## Route handler

Set ```paginate_by=<num>``` in your route handler.

    class FooRoute(ModelRouter):
        ...
        paginate_by=10


## Javascript

Set ```_page=<num>``` when calling get_list

    ...
    var args = {'_page': 1};
    swampDragon.get_list(route, args, callbackName)


## Angular

    var page = 1;
    $dragon.data.getPagedList(route, {}, page).then(function (response) {
        // handle data
    });
