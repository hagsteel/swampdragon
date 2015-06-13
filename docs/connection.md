# Connection


The default connection is specified in settings as

    SWAMP_DRAGON_CONNECTION = ('swampdragon.connections.sockjs_connection.DjangoSubscriberConnection', '/data')


Creating a custom connection requires two steps:

1.  Create the actual connection class
2.  Update `SWAMP_DRAGON_CONNECTION` to `('<path to your connection>', '/data')` in settings


Your connection class should extend `SubscriberConnection` (or another connection that in turn extends `SubscriberConnection`).

The connection class have the following functions that can be overridden:


##  on_open(self, request)

This is called when a client establishes a connection to the SwampDragon server.

The request object is not a Django http request, rather a Tornado http request.
Cookies etc. is still available.


##  send_heartbeat()

If heartbeats are enabled, this will call `self.send({'heartbeat': '1'})`.
Note that the number 1 has no particular meaning so this could be customised to send whatever data desired.

Note that SockJS has it's own heartbeat that is not directly related to this. 
Generally this heartbeat can be less frequent.


#  on_heartbeat()

This is triggered every time a client responds to a heartbeat.


## on_close(self)

This is called when a client disconnects.


## on_message(self, data)

This is a raw message from the client. By default heartbeats are checked here 
(a check to see if the message is `{'heartbeat': '1'}` so in this instance the number matters).

