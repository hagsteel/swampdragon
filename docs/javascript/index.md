# JavaScript

**note** if you are using a version before 0.4.0 use the legacy documentation


## Setup

Add the following code to your template:

    :::html
    {% load swampdragon_tags %}
    
    <html>
    <body>
    ...
    {% swampdragon_settings %}
    <script type="text/javascript" src="{% static 'swampdragon/js/dist/swampdragon.min.js` %}"></script>
    </body>
    </html>    


and make sure you have `DRAGON_URL` setup in your settings.

For local development: `DRAGON_URL='http://localhost:9999/'`.


## Usage

Before calling a router, ensure that a connection is established 
    
    :::javascript
    swampdragon.ready(function () {
        // connection established
        // call subscribe or any other router calls
    });


## Args

These are the most common args:

*  `route`: the name of your router (declared as `route_name` on the router)
*  `data`: a dictionary of data to pass to the router
*  `success`: a callback that takes two arguments: `context`, `data` where data is any data sent by the router
*  `failure`: a callback that takes two arguments: `context`, `data` where data contains the error message(s)


### Subscribe / unsubscribe

To start listening to a channel call `subscribe`:

    :::javascript
    
    // Subscribing to all channels provided by the foo-router
    swampdragon.subscribe('foo-route', 'local-channel', null, function (context, data) {
        // successfully subscribed
    }, function (context, data) {
        // subscription failed
    });

    // Unsubscribe
    swampdragon.unsubscribe('foo-route', 'local-channel', null, function (context, data) {
        // successfully unsubscribed
    }, function (context, data) {
        // unsubscribe failed
    });
    
   
`unsubscribe` will happen automatically if the connection is closed. If the browser window is closed or the user navigates away from the page


### On channel message

Args: `channels`, `message`

`channels` is a list of your channels (not the server channels, your local channels)
`message` is the data provided by the server

    :::javascript
    swampdragon.onChannelMessage(function (channels, message) {
        // 
    });

`onChannelMessage` is triggered every time some data is published.


### Call router

There are predefined functions for getting lists, objects, creating and updating etc.
Some times these functions doesn't suit your application. In these instances use `callRouter`.

An example router that adds one to any value it's passed 


    :::python
    class FooRouter(BaseRouter):
        route_name = 'foo-router'
        valid_verbs = ['add_one']
        
    def add_one(self, value):
        self.send({'result': value + 1})
        

The following JavaScript will call `add_one` and log the value to the console


    :::javascript
    swampdragon.callRouter('add_one', 'foo-router', {value: 10}, function (context, data) {
        console.log(data.result);
    });
    
    
### Pre-defined functions for handling models

In the case of a `ModelRouter` (or `ModelPublisherRouter`) there are pre-defined functions to handle manipulating instances of the model.


#### getSingle

`getSingle` asks for one instance of a model.

Args: `route`, `data`, `success`, `failure`


    :::javascript
    swampdragon.getSingle(route, data, function (context, data) { ... }, function (context, data) { ... } );


#### getList

`getList` asks for a list of instances of a model.

Args: `route`, `data`, `success`, `failure`


    :::javascript
    swampdragon.getList(route, data, function (context, data) { ... }, function (context, data) { ... } );


#### getPagedList

`getPagedList` asks for a paged list of instances of a model.

Args: `route`, `data`, `page`, `success`, `failure`

If no `page` argument is supplied it will default to one.


    :::javascript
    var pageNumber = 12;
    swampdragon.getPagedList(route, data, pageNumber, function (context, data) { ... }, function (context, data) { ... } );


#### create

`create` an instance of a model 

Args: `route`, `data`, `page`, `success`, `failure`


    :::javascript
    var data = {some_value: 12, other_value: 'hello world'};
    swampdragon.create(route, data, function (context, data) { ... }, function (context, data) { ... } );


By default `create` will respond with an instance of the newly created model (or errors if model creation failed)



#### update

`update` an instance of a model

Args: `route`, `data`, `page`, `success`, `failure`


    :::javascript
    var data = {some_value: 12, other_value: 'hello world', id: 123};
    swampdragon.update(route, data, function (context, data) { ... }, function (context, data) { ... } );


#### delete

`delete` an instance of a model

Args: `route`, `data`, `page`, `success`, `failure`


    :::javascript
    var data = {id: 123};
    swampdragon.delete(route, data, function (context, data) { ... }, function (context, data) { ... } );
