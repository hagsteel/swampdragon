SwampDragon
===========

[![Downloads](https://pypip.in/download/SwampDragon/badge.svg?style=flat&?period=month)](https://pypi.python.org/pypi/SwampDragon/)
[![Downloads](https://pypip.in/py_versions/SwampDragon/badge.svg?style=flat&)](https://pypi.python.org/pypi/SwampDragon/)

Build real-time web applications with Django.

Features:

*  Real-time data
*  Self publishing model
*  Make use of the wonderful features of Django
*  Serializers handling Django models
*  Customisable field serializers
*  Routers that are easy to understand
*  Angular JS support
*  Query style data subscriptions
*  Easy to implement in existing Django projects


SwampDragon makes use of Djangos wonderful ORM, Tornados excellent websocket support (with fallback. Tested in IE7), and
Redis blazing speed.

## Installation

    pip install swampdragon
    
   
## Quickstart

See [documentation](http://swampdragon.net/documentation/) and example projects in this repository.

[Tutorial](http://swampdragon.net/tutorial/part-1-here-be-dragons-and-thats-a-good-thing/) available here.

# Documentation

See [Documentation](http://swampdragon.net/documentation/) here


# Changelog

See change logs at [swampdragon.net](http://swampdragon.net/changelog/) here


### JavaScript changes

The old ```dataService``` will be removed.
 

#### AngularJS
With multiple endpoint support, the AngularJS service changes. 

```dataService``` is renamed to ```$dragon``` 

and all calls requires the endpoint. So ```dataService.getList``` becomes ```$dragon.data.getList``` 
(where **data** is the name of the endpoint).

Previously $rootScope was used to broadcast when the connection was ready, however with multiple connections
possible this now changes to ```$dragon.[endpoint].onReady```

    $dragon.data.onReady(function() {
        ...
    });


The same goes for ```onChannelMessage```.

    // Previously
    $scope.$on('handleChannelMessage', function(e, channels, message) { ... });
    
    // Now
    $dragon.data.onChannelMessage(function(channels, message) { ... });


#### JavaScript settings 

Settings needs to be included in the template
 
    <script type="text/javascript" src="http://localhost:9999/settings.js"></script>
    
(remember to change localhost to your server url / domain name)
