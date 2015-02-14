var messageHandler = function (e) {
    if ('data' in e) {
        if ((typeof e.data != "object")) {
            e['data'] = JSON.parse(e['data']);
        }
    }

    /*******************
     * Callback
     *******************/
    if ('data' in e && 'context' in e.data && 'client_callback_name' in e.data.context) {
        swampDragon.emit(e.data.context.client_callback_name, [e.data.context, e.data.data]);
    }

    /*******************
     * Channel setup
     *******************/
    if ('channel_data' in e.data) {
        var channel_setup = e.data.channel_data;
        for (i in channel_setup.remote_channels) {
            remote_chan = channel_setup.remote_channels[i];
            if (!(remote_chan in swampDragon.channels)) {
                swampDragon.channels[remote_chan] = []
            }
            if (!(channel_setup.local_channel in swampDragon.channels[remote_chan])) {
                swampDragon.channels[remote_chan].push(channel_setup.local_channel);
            }
        }

        if (!(channel_setup.local_channel in swampDragon.channels)) {
            swampDragon.channels[channel_setup.remote_channel] = channel_setup.local_channel;
        }
    }

    /*******************
     * Channel message
     *******************/
    if ('channel' in e.data) {
        var channel = swampDragon.channels[e.data.channel];
        delete(e.data['channel']);
        swampDragon.settings.onchannelmessage(channel, e.data);
        return;
    }

    /*******************
     * Heartbeat
     *******************/
    if ('data' in e && 'heartbeat' in e['data']) {
        if (e.data.heartbeat == 1) {
            swampDragon.send(JSON.stringify(e.data));
            swampDragon.settings.onheartbeat();
        }
    }
    settings.onmessage(e);
};

module.exports  = messageHandler;
