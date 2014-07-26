# Sessions

Storing values for a period of time is done in the session store.
The default session store is RedisSessionStore, which reads and writes to Redis

To create your own session store, inherit from ```BaseSessionStore```.

Assign the store by setting ```DRAGON_SESSION_STORE``` in your settings file.

i.e DRAGON_SESSION_STORE = 'app.session_store.FooSessionStore'

You have to implement the expiration procedure manually.

Implementing your own session store requires two functions:

    class FooSessionStore(object):
        def save(self, key, val):
            ...
    
        def get(self, key):
            ...

The function ```save_get_key(self, val):``` will generate a UUID as a key and return the key.

This is a convenience method to avoid creating unique keys every time a new object is saved to session.

To generate your own keys, override ```def save_get_key(self, val):```.

## Session refresh

Currently there is no built in way to refresh the expiration of a session.
You manually have to handle keeping the session alive.

One way of doing this would be to ues the heartbeat functionality

In this example we create a data connection.

When the connection is open, we start a periodic callback (import ```from tornado.ioloop import PeriodicCallback```).
We set the callback to occur every 10 minutes, where we send a heartbeat message to the client.
The client is expected to send a heartbeat message back, containing the session key.
If the session key is available: call ```refresh_key_timeout``` on the session store.


    class DataConnection(SubscriberConnection):
        def on_open(self, request):
            super(DataConnection, self).on_open(request)
            self.session_store = get_session_store()
            self.start_heartbeat()
            self.periodic_callback = None

        def on_close(self):
            super(DataConnection, self).on_close()
            self.periodic_callback.stop()

        def start_heartbeat(self):
            ms_minute = 1000 * 60
            self.periodic_callback = PeriodicCallback(self.on_heartbeat, ms_minute * 10)
            self.periodic_callback.start()

        def on_heartbeat(self):
            self.send({'heartbeat': 'tick'})

        def on_message(self, data):
            if 'heartbeat' in data:
                try:
                    json_data = json.loads(data)
                    self.session_store.refresh_key_timeout(json_data['session'])
                    return
                except:
                    pass
            super(DataConnection, self).on_message(data)


When instantiating the SwampDragon javascript object, there is an optional callback
call ```onheartbeat```, that can be used to react on a heartbeat message and send the session key
to the server.

Note: the angular service will issue ```$rootScope.$broadcast('heartbeat');``` on this event.
