# Pagination


## Route handler

Adding pagination is simple.

Set ```paginate_by=<num>``` in your route handler.

    class FooRoute(BaseModelRouter):
        ...
        paginate_by=10


## Javascript

Set ```_page=<num>``` when calling get_list

    ...
    var args = {'_page': 1};
    swampDragon.get_list(route, args, callbackName)


## Angular

        var page = 1;
        dataService.getPagedList(route, {}, page).then(function (response) {
            // handle data
        });
