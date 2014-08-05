Swamp Dragon
============

Build realtime applications with Django.


# UNDER DEVELOPMENT


# Important
**Note**: As Django models are blocking, long queries will prevent other requests from coming through.


# Tornado 4.0
If you experience ```Error during WebSocket handshake: Unexpected response code: 403``` you might have to run 
the latest dev version of sockjs-tornado.

```pip uninstall sockjs-tornado```


```pip install -e git+https://github.com/mrjoes/sockjs-tornado.git#egg=sockjs-tornado```

This should solve the error message.


# Documentation

see [ReadTheDocs](http://swamp-dragon.readthedocs.org)
