require('sockjs'); // browserify shim

var eventHandler = require('./event-handler'),
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


function onopen () {
    connectionAttempt = 0;
    isReady = true;
    eventHandler.emit('open');
    eventHandler.emitOnce('ready');
}


function onclose (data) {
    connection.socket = null;
    isReady = false;
    if (connectionAttempt === 0) {
        eventHandler.emit('close');
    }

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

        channels.setupChannels(channel_setup);
    }

    /*******************
     * Channel message
     *******************/
    if ('channel' in e.data) {
        var localChannels = channels.getLocalChannels(e.data.channel);
        delete(e.data['channel']);
        eventHandler.emit('channelMessage', [localChannels, e.data]);
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
