# DataMapper

The ```DataMapper``` is used to map model data.

When calling ```subscribe``` on a model router, it will answer with an object map.

    :::javascript
    swampdragon.subscribe('foo-route', 'local-channel', null, function (context, data) {
        this.dataMapper = new DataMapper(data);
    });
    
    swampdragon.onChannelMessage(function (channels, message) {
        for(var i in channels) {
            if (channels[i] == 'news') {
                this.news = this.dataMapper.mapData(this.news, message.data);
            }
        }
    });
        

**Note**: only model routers will respond with an object map by default.
