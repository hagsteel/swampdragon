# AngularJS and SwampDragon #


## Getting started ##

Include the following in your template

```html
<!-- AngularJS -->
<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/angularjs/1.2.21/angular.min.js"></script>

<!-- Swamp dragon -->
<script type="text/javascript" src="http://localhost:9999/settings.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/vendor/sockjs-0.3.4.min.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/swampdragon.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/datamapper.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/angular/services.js"></script>
```


### Setting up your AngularJS app ###

Include the `SwampDragonServices` services.


```javascript
var FooApp = angular.module('FooApp', [
    'SwampDragonServices',
    'FooControllers'
]);
```


### Adding your controller ###

The following controller will listen to updates from the foo-router and map the data.
Make sure to inject `dataService` into your controller.


```javascript
var FooControllers = angular.module('FooControllers', []);

FooControllers.controller('FooCtrl', ['$scope', '$dragon', function($scope, $dragon) {
    $scope.channel = 'foo-chan';
    $scope.foos = [];

    $dragon.data.onReady(function() {
        $dragon.data.subscribe('foo-router', $scope.channel, {})
            .then(function(response) {
                // this assume the foo-router is a ModelRouter
                // or a ModelPublisherRouter
                $scope.dataMapper = new DataMapper(response.data);
            }
        );
    });

    $dragon.data.onChannelMessage(function(channels, message) {
        if (indexOf.call(channels, $scope.channel) > -1) {
            $scope.$apply(function() {
                $scope.dataMapper.mapData($scope.foos, message.data);
            });
        }
    });

}]);
```


### Html template ###

If you are mixing your AngularJS into a Django template, make sure to use the `{% verbatim %}` tag.

```html
<div ng-controller="FooCtrl">
    <ul>
        <li ng-repeat="foo in foos">{{ foo }}</li>
    </ul>
</div>
```


## `SwampDragonServices`

Unlike the conventional JavaScript solution, the `SwampDragonServices` returns promises.
This means that there is no need to map callbacks.

```javascript
$dragon.data.getSingle('foo-router', {}).then(function(response) {
    var data = response.data;
});
```

`$dragon` needs to be injected into the controller.

```javascript
FooControllers.controller('FooCtrl', ['$dragon', function($dragon) { ... }]);
```


### `onReady`

To react once SwampDragon is connected

```javascript
$dragon.data.onReady(function() {
    // Call router with dragonService
});
```

This way calls won't be made to a router before a connection is established.


### `callRouter`

`callRouter` is similar to the non-AngularJS version, except it return a promise.

```javascript
$dragon.data.callRouter('say-hello', 'hello-router').then(function(response) {
    console.log(response.data);
}).except(function(errors) {
    console.log(errors);
});
```

Note that older versions of IE use ECMAScript 3, so `then(...).except(...)` will fail.
This is not a shortcoming in SwampDragon or AngularJS, and this can be solved by using brackets instead

```javascript
$dragon.data.callRouter('say-hello', 'hello-router').then(function(response) {
    console.log(response.data);
})["except"](function(errors) {
    console.log(errors);
});
```


### `getSingle`

This will request a single instance of an object

```javascript
$dragon.data.getSingle('foo-router', {}).then(function(response) {
    console.log(response.data); // an instance of Foo
});
```


### `getList`

This requests a list of objects from a router

```javascript
$dragon.data.getList('foo-router').then(function(response) {
    console.log(response.data); // a list of Foo
});
```


### `createObject`

Request that a router creates an object.

```javascript
$dragon.data.createObject('foo-router', {bar: 'foo bar'}).then(function(response) {
    console.log(response.data); // a newly created Foo
});
```


### `updateObject`

Request that a router updates an object.

```javascript
$dragon.data.updateObject('foo-router', {bar: 'updated bar', id: 3})
    .then(function(response) {
        console.log(response.data); // an created Foo
    }
);
```


### `deleteObject`

Request that a router deletes an object.

```javascript
$dragon.data.deleteObject('foo-router', {id: 3}).then(function(response) {
    console.log(response.data); // The deleted Foo
});
```


### `subscribe`

Subscribe to a channel.

```javascript
$dragon.data.subscribe('foo-router', $scope.channel, {}).then(function(response) {
    $scope.dataMapper = new DataMapper(response.data);
});
```
If the router is not a model router, the response is not necessarily an object map.


### `unsubscribe`

Unsubscribe from a channel.

```javascript
$dragon.data.unsubscribe('foo-router', $scope.channel, {});
```


### `handleChannelMessage`

Whenever a new channel message arrives, the dataService will emit `handleChannelMessage`.

```javascript
$dragon.data.onChannelMessage(function(e, channels, message) { ... });
```
If a `DataMapper` is present

```javascript
$dragon.data.onChannelMessage(function(e, channels, message) {
    if (indexOf.call(channels, $scope.channel) > -1) {
        $scope.$apply(function() {
            $scope.dataMapper.mapData($scope.foos, message.data);
        });
    }
});
```