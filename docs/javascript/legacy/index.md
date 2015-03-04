# JavaScript (pre version 0.4.0) #

SwampDragon comes with an AngularJS service and directives, but it works just as well with other JavaScript libraries, or in fact, no library at all.

For AngularJS see [SwampDragon and AngularJS](/documentation/angularjs-and-swampdragon/).

There are 4 callbacks that can be passed as parameters when instantiating SwampDragon.

*  `onopen`
*  `onmessage`
*  `onchannelmessage`
*  `onclose`

The minium required script includes to use SwampDragon

```html
<!-- Swamp dragon -->
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/vendor/sockjs-0.3.4.min.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/swampdragon.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/datamapper.js"></script>
```

If you are using `ModelRouter` or `ModelPublisherRouter` it's recommended to include the DataMapper as well.

```html
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/datamapper.js"></script>
```

A vanilla JavaScript wrapper was added as of version 0.3.8 to avoid the awkward callback setup

```html
<script type="text/javascript" src="{{ STATIC_URL }}swampdragon/js/swampdragon-vanilla.js"></script>
```


## Creating a connection ##

```javascript
function onOpen() { ... }
function onMessage() { ... }
function onChannelMessage() { ... }
function onClose() { ... }

var swampDragon = new SwampDragon({
    onopen: onOpen,
    onmessage: onMessage,
    onchannelmessage: onChannelMessage,
    onclose: onClose
});

swampDragon.connect('http://' + window.location.hostname + ':9999', 'data')
```

Note that once `new SwampDragon(...)` is called, it will assign an instance to `window.swampDragon` so there is no need to do this manually.

See documentation on [callbacks](/documentation/javascript-callbacks/)


## Calling routers ##

SwampDragon have a few functions

*  `disconnect`     (disconnect from the server)
*  `callRouter`     (call a router)
*  `get_single`     (call a router to get a single object)
*  `get_list`       (call a router to get a list of objects)
*  `create_object`  (call a router with data and ask it to create an object)
*  `update_object`  (call a router with data and ask it to update an object)
*  `delete_object`  (call a router with data and ask it to delete an object)
*  `subscribe`      (subscribe to a channel)
*  `unsubscribe`    (unsubscribe from a channel)

See documentation on [calling routers](/documentation/javascript-calling-routers/)
