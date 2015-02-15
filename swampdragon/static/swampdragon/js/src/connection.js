require('sockjs'); // browserify shim

var eventHandler = require('./event-handler'),
    messagehandler = require('./message-handler'),
    channels = require('./channels'),
    connection = {},
    isReady = false,
    connectionAttempts = 0;


/********************************
 * Get the host and end point
 ********************************/
function getHost() {
    var host = window.swampdragon_host,
        endpoint = window.swampdragon_settings.endpoint;

    if (endpoint.indexOf('/') != 0) {
        endpoint = '/' + endpoint
    }

    host = host + endpoint;
    return host;
}

function connect () {
    connection.socket = new SockJS(getHost());
    connection.socket.onopen = onopen;
    connection.socket.onclose = onclose;
    connection.socket.onmessage = onmessage;
}


function onopen (callback) {
    connectionAttempt = 0;
    isReady = true;
    eventHandler.emit('open');
}


function onclose (data) {
    connection.socket = null;
    isReady = false;

    if (data.code == 3001) {
        // The connection was aborted.
        // Will not reconnect
        return;
    }

    setTimeout(function() {
        if (connectionAttempt < 10) {
            connectionAttempt++;
            connect();
        }
    }, (connectionAttempt * 500) + 100);

}

function onmessage (e) {
    if ('data' in e) {
        if ((typeof e.data != "object")) {
            e['data'] = JSON.parse(e['data']);
        }
    }

    /*******************
     * Callback
     *******************/
    if ('data' in e && 'context' in e.data && 'client_callback_name' in e.data.context) {
        eventHandler.emit(e.data.context.client_callback_name, [e.data.context, e.data.data]);
    }

    /*******************
     * Channel setup
     *******************/
    if ('channel_data' in e.data) {
        var channel_setup = e.data.channel_data,
            remote_chan;
        for (i in channel_setup.remote_channels) {
            remote_chan = channel_setup.remote_channels[i];
            if (!(remote_chan in channels)) {
                channels[remote_chan] = []
            }
            if (!(channel_setup.local_channel in channels[remote_chan])) {
                channels[remote_chan].push(channel_setup.local_channel);
            }
        }

        if (!(channel_setup.local_channel in channels)) {
            channels[channel_setup.remote_channel] = channel_setup.local_channel;
        }
    }

    /*******************
     * Channel message
     *******************/
    if ('channel' in e.data) {
        var channel = channels[e.data.channel];
        delete(e.data['channel']);
        eventHandler.emit('channelMessage', [channel, e.data]);
        return;
    }

    /*******************
     * Heartbeat
     *******************/
    if ('data' in e && 'heartbeat' in e['data']) {
        if (e.data.heartbeat == 1) {
            connection.socket.send(JSON.stringify(e.data));
            eventHandler.emit('heartbeat', [channel, e.data]);
            return;
        }
    }
    eventHandler.emit('message', e);
}

connect();

module.exports = {
    sockjs: connection,
    onopen: connection.onopen,
    send: connection.send,
    ready: function () {
        return isReady;
    },
    on: eventHandler.on
};
