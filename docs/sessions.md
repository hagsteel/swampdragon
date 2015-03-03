# Sessions

By default SwampDragon use Redis for storing session data.
This means only strings and dictionaries can be stored.

Sessions are per-connection, which means if the user is disconnected the session data is lost.


Use ```SWAMP_DRAGON_SESSION_STORE``` to create your own custom session store.

**Note** that heartbeats need to be enabled for session refresh to work.
Set ```SWAMP_DRAGON_HEARTBEAT_ENABLED = True``` to enable heartbeats.


To change the heartbeat frequency from the default 20 minutes, set ```SWAMP_DRAGON_HEARTBEAT_FREQUENCY``` to the number of milliseconds
between heartbeats.


## Creating a custom session store

The following code snippet provides a session that only works for signed in users, but unlike the current sessions these sessions
would not disappear as when a connection is lost.

```python

from swampdragon.pubsub_providers.redis_publisher import get_redis_cli
from swampdragon.sessions.session_store import BaseSessionStore


class UserOnlyCustomSession(BaseSessionStore):
    key_expires = 30  # seconds

    def __init__(self, connection):
        super(UserOnlyCustomSession, self).__init__(connection)
        self.keys = []
        self.redis_client = get_redis_cli()

    def compose_key(self, key):
        if not self.connection.user:
            return None
        return 'uid:{}|key:{}'.format(self.connection.user.pk, key)

    def get(self, key):
        complete_key = self.compose_key(key)
        if not complete_key:
            return None
        return self.redis_client.get(complete_key)

    def set(self, key, val):
        complete_key = self.compose_key(key)
        if not complete_key:
            return
        self.redis_client.set(complete_key, val)
        self.redis_client.expire(complete_key, self.key_expires)

    def refresh_key_timeout(self, key):
        complete_key = self.compose_key(key)
        self.redis_client.expire(complete_key, self.key_expires)
```

The next step is to tell SwampDragon about this session store.

Update ```SWAMP_DRAGON_SESSION_STORE``` settings to use your new settings

```python

SWAMP_DRAGON_SESSION_STORE = 'myproject.myapp.custom_session.UserOnlyCustomSession'
```

This tells SwampDragon to use the new session store instead of the default Redis session store.


## Notes about sessions spanning connections

The above example works on the premise that a user is signed in and the connection has a user (this can be achieved using swampdragon-auth).
Is would be possible to create a session store that works even though a connection is lost and re-established, though such an
implementation is very application specific.

There is a myriad of ways this could be implemented.

One such workflow would be as follows:

1.  In the Django view set a (http) cookie with a session id (unless one exists)
2.  In the template: output a hidden field with the session id
3.  Pass the session id to a router. The router can then attach the session key to the connection
4.  Create a custom session store that makes use of the session key

However, this is a very specific implementation thus will not be provided by SwampDragon.
