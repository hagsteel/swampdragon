# Settings

Add 

    # SwampDragon settings
    SWAMP_DRAGON_CONNECTION = ('swampdragon.connections.sockjs_connection.DjangoSubscriberConnection', '/data')
  
to your settings file.


## Available settings

### ```SWAMP_DRAGON```

This is a dictionary with all the settings you want to expose to the client (these settings are available in JavaScript on the client site).


### ```SWAMP_DRAGON_HEARTBEAT_ENABLED```

If set to ```True``` heartbeats will be enabled


### ```SWAMP_DRAGON_HEARTBEAT_FREQUENCY```

This is the frequency of heartbeats set in milliseconds.
The default is ```1000 * 60 * 20``` (20 minutes)


### ```SWAMP_DRAGON_SESSION_STORE```

You can easily create and add your own custom session store (see the documentation for sessions).


### ```SWAMP_DRAGON_REDIS_HOST```

Redis host, default is localhost


### ```SWAMP_DRAGON_REDIS_PORT```
 
Redis port, default is 6379


### ```SWAMP_DRAGON_REDIS_DB```

Redis database number, default is 0. 

**Note** that this does not have any effect on Redis PUBSUB.


### ```SWAMP_DRAGON_HOST```

This setting will override the default `localhost` host


### ```SWAMP_DRAGON_PORT```

This setting will override the default `9999` port


## JavaScript settings (settings exposed to clients via JavaScript)

By adding
    
    :::html
    {% load swampdragon_tags %}
    
    <html>
    <body>
    ...
    {% swampdragon_settings %}
    </body>
    </html>
        
to your template, you can access SwampDragon specific settings within your JavaScript.

You can expose your own settings by setting ```SWAMP_DRAGON``` to a dictionary in your (Django) settings.py file.

    SWAMP_DRAGON = {
        'foo': 'bar',
    }

These settings are available  from ```window.swampdragon_settings```.

    <script>
        console.log(window.swampdragon_settings.foo); // output bar
    </script>
    
    
If you want to access the url for your SwampDragon instance from JavaScript, you can do so with ```window.swampdragon_host```.

    <script>
        // ouput http://localhost:9999 assuming you are running your server on that url
        console.log(window.swampdragon_host); 
    </script>
    
