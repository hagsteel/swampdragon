/*
 * SwampDraon 0.2 connection wrapper around SocketJS
 * By Jonas Hagstedt, 2014
 * -----------------------------------
 * Usage:
 * var swampDragon = SwampDragon(options);
 * swampDragon.connect();
 * Options:
 * onopen: function() called when a connection is established
 * onclose: function() called when the connection is closed
 * onmessage: function(e) called when a message is received from the server. e.data contains the message
 * onchannelmessage: function(channel, data) called when a channel receives a message
 * -----------------------------------
 */
var SwampDragon = function(options) {
    options = options || {};
    var swampDragon = this;
    swampDragon.isReady = false;
    window.swampDragons = window.swampDragons || {};
    swampDragon.conn = null;
    swampDragon.host = null;
    swampDragon.channels = {};
    swampDragon.connectionAttempt = 0;

    swampDragon.defaultOnOpen = function() {  };
    swampDragon.defaultOnMessage = function(e) { };
    swampDragon.defaultOnHeartbeat = function(e) { };
    swampDragon.defaultOnChannelMessage = function(channel, data) { };
    swampDragon.defaultOnClose = function(data) {
        swampDragon.conn = null;
        swampDragon.isReady = false;

        if (data.code == 3001) {
            // The connection was aborted.
            // Will not reconnect
            return;
        }

        setTimeout(function() {
            if (swampDragon.connectionAttempt < 10) {
                swampDragon.connectionAttempt++;
                swampDragon.connect();
            }
        }, (swampDragon.connectionAttempt * 500) + 100);
    };
    swampDragon.defaultLoginRequired = function() { };

    var settings = {
        onopen: swampDragon.defaultOnOpen,
        onmessage: swampDragon.defaultOnMessage,
        onchannelmessage: swampDragon.defaultOnChannelMessage,
        onclose: swampDragon.defaultOnClose,
        onloginrequired: swampDragon.defaultLoginRequired,
        onheartbeat: swampDragon.defaultOnHeartbeat
    };

    swampDragon.settings = settings;

    if ('onopen' in options) {
        swampDragon.settings.onopen = options.onopen;
    }

    if ('onmessage' in options) {
        swampDragon.settings.onmessage = options.onmessage;
    }

    if ('onchannelmessage' in options) {
        swampDragon.settings.onchannelmessage = options.onchannelmessage;
    }

    if ('onclose' in options) {
        swampDragon.settings.onclose = options.onclose;
    }

    if ('onloginrequired' in options) {
        swampDragon.settings.onclose = options.onloginrequired;
    }

    if ('onheartbeat' in options) {
        swampDragon.settings.onheartbeat = options.onheartbeat;
    }

    swampDragon.connect = function(url, channel) {
        window.swampDragons[channel] = swampDragon;
        swampDragon.url = url;
        swampDragon.disconnect();
        if (swampDragon.host == null) {
            if (channel.indexOf('/') != 0) {
                channel = '/' + channel
            }
            swampDragon.host = url + channel;
        }
        swampDragon.conn = new SockJS(swampDragon.host);

        swampDragon.conn.onopen = function() {
            swampDragon.connectionAttempt = 0;
            swampDragon.isReady = true;
            swampDragon.settings.onopen();
        };

        swampDragon.conn.onmessage = function(e) {
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
        swampDragon.conn.onclose = swampDragon.settings.onclose;
    };

    swampDragon.disconnect = function() {
        if (swampDragon.conn != null) {
            swampDragon.conn.close();
            swampDragon.conn = null;
            swampDragon.isReady = false;
        }
    };

    swampDragon.send = function(data) {
        return swampDragon.conn.send(data);
    };

    swampDragon.sendJSON = function (data) {
        return swampDragon.send(JSON.stringify(data));
    };

    swampDragon.get_single = function(route, args, callbackName) {
        return swampDragon.callRouter('get_single', route, args, callbackName);
    };

    swampDragon.get_list = function(route, args, callbackName) {
        return swampDragon.callRouter('get_list', route, args, callbackName);
    };

    swampDragon.create_object = function(route, args, callbackName) {
        return swampDragon.callRouter('create', route, args, callbackName);
    };

    swampDragon.update_object = function(route, args, callbackName) {
        return swampDragon.callRouter('update', route, args, callbackName);
    };

    swampDragon.delete_object = function(route, args, callbackName) {
        return swampDragon.callRouter('delete', route, args, callbackName);
    };

    swampDragon.subscribe = function(route, args, callbackName, channel) {
        return swampDragon.callRouter('subscribe', route, args, callbackName, channel);
    };

    swampDragon.unsubscribe = function(route, args, callbackName, channel) {
        return swampDragon.callRouter('unsubscribe', route, args, callbackName, channel);
    };

    swampDragon.callRouter = function(verb, route, args, callbackName, channel) {
        if (channel != null) {
            args = args || {};
            args['channel'] = channel
        }
        return swampDragon.sendJSON({
            route: route,
            verb: verb,
            args: args,
            callbackname: callbackName
        });
    };

    // Event emitter
    swampDragon.events = {};
    swampDragon.on = function(name, fn) {
        swampDragon.events[name] = swampDragon.events[name] || [];
        swampDragon.events[name].push(fn);
    };

    swampDragon.emit = function(name, args) {
        swampDragon.events[name] = swampDragon.events[name] || [];
        args = args || [];
        for (var ev in swampDragon.events[name]) {
            var fn = swampDragon.events[name][ev];
            fn.apply(this, args);
        }
    };

    return swampDragon;
};

