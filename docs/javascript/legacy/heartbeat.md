# Heartbeat implementation #

Sometimes it's useful to implement a heartbeat (for instance if you implement your own authentication solution)

To enable heartbeats add `SWAMP_DRAGON_HEARTBEAT_ENABLED = True` to settings.py.

**Note** that heartbeats need to be enabled for session refresh to work.


## JavaScript ##

If you want to perform a custom action in JavaScript for each heartbeat, implement the `onHeartbeat` function

```javascript
$dragon.onHeartbeat(function() {
    console.log('heartbeat');
});
```

## Custom connection ##

If you have a custom connection and want to execute some code on each beat, override `on_heartbeat`.

 ```javascript
def on_heartbeat(self):
    super().on_heartbeat()
    # Your functionality here
```

**Note** that if you don't call `super` on the heartbeat the session keys will not refresh
(this is only relevant if you use sessions)
