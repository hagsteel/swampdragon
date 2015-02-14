# DataMapper

The ```DataMapper``` is used to map model data.

When calling ```subscribe``` on a model router, it will answer with an object map.

    window.swampDragon.on('subscribeCallback', function(context, data) {
        this.dataMapper = new DataMapper(data);
    });
    window.swampDragon.subscribe('news', {}, 'subscribeCallback', 'news');
    
    function onChannelMessage(channels, message) {
        for(var i in channels) {
            if (channels[i] == 'news') {
                this.news = this.dataMapper.mapData(this.news, message.data);
            }
        }
    };

Note that only model routers will respond with an object map by default.
