# Callbacks

## Onopen

Onopen takes no arguments.

    function onOpen() { ... }

It is triggered as soon as a connection is established.

To prevent calling SwampDragon prematurely, this is a good place to notify your application that it can now start communicating with SwampDragon.

    function ready() {
        // SwampDragon is now ready 
        window.swampDragon.callRouter(...);
    }
    
    function onOpen() {
        ready();
    }
    
    new SwampDragon({onopen: onOpen});
    swampDragon.connect('http://' + window.location.hostname + ':9999', 'data')

## Onmessage

Onmessage takes one argument 

    function onMessage(message) { ... }

Each message contains a ```data``` property, where the relevant data resides.

```message.data.context``` contains the context of the message:

*  verb (this is the verb that was called on the router)
*  client_callback_name (this is the callback that should be triggered in response to the call)
*  state (this is either ```success``` or ```error```)

    
```message.data.data``` contains what ever route specific message the server sends
    
```message.data.channel_data``` contains data related to a channel, if present (there is usually no need to handle this data). 


Example data
    
    {
        "type": "message",
        "data": {
            "context": {
                "verb": "subscribe",
                "client_callback_name": "myCallback-00001",
                "state": "success"
            },
            "data": "subscribed",
            "channel_data": {
                "local_channel": "mychan",
                "remote_channels": [
                    "remote-channel"
                ]
            }
        }
    }    


### Important note about callbacks

Because SwampDragon is not a request/response solution, callbacks might occur in a different order than the messages were sent.

Therefore the server accepts a callback name when the client sends a message, and the callback name will be included when the server submits data.

There are two obvious solutions to handle this:

**1.**

    // In this scenario we generate a callback name and listen for that name 
    // with the swampDragon.on function.
    // The benefit of this approach is the callback being handled inside the calling function.
    function generateCallbackName() {
        var callbackName = 'cb_' + window._callbackId;
        window._callbackId++;
        if (this._callbackId > 9999)
            this._callbackId = 0;
        return callbackName;
    }
    
    function blueButtonClicked(evt) {    
        var callbackName = generateCallbackName();
        swampDragon.on(callbackName, function(context, data) { ... });
        swampDragon.callRouter(verb, route, args, callbackName, channel);
    }

    function redButtonClicked(evt) {    
        var callbackName = generateCallbackName();
        swampDragon.on(callbackName, function(context, data) { ... });
        swampDragon.callRouter(verb, route, args, callbackName, channel);
    }


**2.**

    // In this scenario we create a callback dictionary.
    // We map the two different callbacks to names.
    // This example is easier to read but in a larger project the callbackMap
    // might become unwieldy
    function redButtonCallback(message) { ... }
    function blueButtonCallback(message) { ... }

    var callbackMap = {
        'red': redButtonCallback,  
        'blue': blueButtonCallback
    };
    
    function redButtonClick() {
        window.swampDragon.callRouter(verb, route, args, 'red');
    }

    function blueButtonClick() {
        window.swampDragon.callRouter(verb, route, args, 'blue');
    }
    
    function onMessage(message) {
        var callback = callbackMap[message.data.context.client_callback_name];
        callback(message.data);
    }


## Onchannelmessage

This is called when a broadcast message is received.

    function onChannelMessage(channels, message) { ... }

```channels``` is a list of channels defined by the client, and the ```message``` is whatever data the server has published to that channel.

### Example 

    function subscribe() {
        // Subscribe to the music channel 
        window.swampDragon.on('callbackA', function(context, data) { ... })
        window.swampDragon.subscribe('tunes', {}, 'callbackA', 'mymusic');

        // Subscribe to the movie channel
        window.swampDragon.on('callbackB', function(context, data) { ... })
        window.swampDragon.subscribe('movies', {}, 'callbackB', 'mymovies');
    }
    
    function onChannelMessage(channel, message) {
        for (var i in channels) {
            if (channels[i] == 'music') {
                musicUpdate(message.action, message.data);
            }

            if (channels[i] == 'movies') {
                musicUpdate(message.action, message.data);
            }
        }
    }
    
    function musicUpdate(action, data) {
        // Update the music data with the DataMapper
    }
    
    function moviesUpdate(action, data) {
        // Update the movie data with the DataMapper
    }
    
In case the update comes from either a ModelRouter or a ModelPublisherRouter the message contains both data and the action.
The action will be either ```created```, ```updated``` or ```deleted```. 
Note that this isn't necessarily the case when publishing non-model data.

The actions are used with an instance of a DataMapper to handle data.

For more information see [DataMapper](/documentation/javascript-data-mapper/).


## Onclose

This function is called if the connection was closed.
This is a good place to reconnect.

    var connectionAttempts = 0;
    
    function onOpen() {
        connectionAttempts = 0;
    }
    
    function connect() {
        window.swampDragon.connect('http://' + window.location.hostname + ':9999', 'data')
    }
    
    function onClose() {
        if (connectionAttempts < 5) {
            connectionAttempts++;
            window.setTimeout(connect, 2000); // Wait 2 seconds before we try to reconnect
        }
    }
