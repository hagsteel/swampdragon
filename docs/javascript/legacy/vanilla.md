# Vanilla JavaScript #

This was added as of version 0.3.8, to avoid the awkward callback setup.

Each call can accept a `success` and `error` function.


## Getting started ##

Include the following in your template (note that the data mapper is optional)

```html
{% load swampdragon_tags %}

<!-- Swamp dragon -->
{% swampdragon_settings %}
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/vendor/sockjs-0.3.4.min.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/swampdragon.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/datamapper.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/swampdragon-vanilla.js"></script>
```


## Parameter overview ##

*  route: this is the name of the router being called
*  verb: this is the name of the function on the router
*  args: this is a dictionary with key / values, passed to the router
*  success: a function that takes `context` and `data`, executed upon **success** of the router call
*  failure: a function tahat takes `context` and `data`, executed upon **failure** of the router call


## callRouter ##

Parameters: `(verb, route, args, success, failure)`

```javascript
var vanillaDragon = new VanillaDragon();

function success(context, data) {
    ...
}

function fail(context, data) {
    ...
}

vanillaDragon.callRouter('say_hello', 'hello-router', null, success, fail);
```


## getSingle ##

Parameters: `(route, data, success, failure)`

```javascript
var vanillaDragon = new VanillaDragon();
vanillaDragon.getSingle('people', {name__contains:'john'}, function(context, data) { ... });
```


## getList ##

Parameters: `(route, data, success, failure)`

```javascript
var vanillaDragon = new VanillaDragon();
vanillaDragon.getList('people', {name__contains:'john'}, function(context, data) { ... });
```


## getPagedList ##

Parameters: `(route, data, page, success, failure)`

```javascript
var vanillaDragon = new VanillaDragon();
vanillaDragon.getPagedList('people', {name__contains:'john'}, 2, function(context, data) { ... });
```


## create ##

Parameters: `(route, data, success, failure)`

```javascript
var vanillaDragon = new VanillaDragon();
vanillaDragon.create('people', {name:'john'}, function(context, data) { ... }, function(context, data) { ... });
```


## update ##

Parameters: `(route, data, success, failure)`

```javascript
var vanillaDragon = new VanillaDragon();
vanillaDragon.update('people', {name:'john', id:12}, function(context, data) { ... }, function(context, data) { ... });
```


## delete ##

Parameters: `(route, data, success, failure)`

```javascript
var vanillaDragon = new VanillaDragon();
vanillaDragon.delete('people', {id:12}, function(context, data) { ... }, function(context, data) { ... });
```


## subscribe ##

Parameters: `(route, channel, args, success, failure)`

```javascript
var vanillaDragon = new VanillaDragon();
vanillaDragon.subscribe('people', 'interesting-people', {name__contains:'john'}, function(context, data) { ... }, function(context, data) { ... });
```


## unsubscribe ##

Parameters: `(route, channel, args, success, failure)`

```javascript
var vanillaDragon = new VanillaDragon();
vanillaDragon.unsubscribe('people', 'interesting-people', null, function(context, data) { ... }, function(context, data) { ... });
```
