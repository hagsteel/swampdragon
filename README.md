SwampDragon
===========

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


SwampDragon makes use of Djangos wonderful ORM, Tornados excellent websocket support (with fallback. Tested in IE7), and
Redis blazing speed.

## Installation

    pip install swampdragon
    
   
## Quickstart

See documentation and example projects in this repository


## Notes

### Tornado 4.0
If you experience ```Error during WebSocket handshake: Unexpected response code: 403``` you might have to run 
the latest dev version of sockjs-tornado.

```pip uninstall sockjs-tornado```


```pip install -e git+https://github.com/mrjoes/sockjs-tornado.git#egg=sockjs-tornado```


** update ** this seems to have been resolved now



# Documentation

see [ReadTheDocs](http://swamp-dragon.readthedocs.org)
