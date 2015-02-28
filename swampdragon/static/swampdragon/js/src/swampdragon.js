/*
 * SwampDraon connection wrapper around SocketJS
 * By Jonas Hagstedt, 2014
 * -----------------------------------
 * Usage:
 * var swampdragon.ready(function() {});
  * -----------------------------------
 */

var connection = require('./connection');
var eventHandler = require('./event-handler');
var swampdragon = swampdragon || {};


/*********************
 * Connection setup
 *********************/
swampdragon.open = function (fn) {
    if (connection.ready()) {
        fn();
    } else {
        connection.on('open', fn);
    }
};


swampdragon.close = function (fn) {
    connection.on('close', fn);
};


swampdragon.ready = function (fn) {
    if (connection.ready()) {
        fn();
    } else {
        connection.on('ready', fn);
    }
};


swampdragon.onChannelMessage = function (fn) {
    eventHandler.on('channelMessage', fn);
};


/*********************
 * Send data
 *********************/
swampdragon.send = function(data) {
    return connection.sockjs.socket.send(data);
};

swampdragon.sendJSON = function(data) {
    return swampdragon.send(JSON.stringify(data));
};


/*********************
 * Call router
 *********************/
swampdragon.callRouter = function (verb, route, args, success, failure, channel) {
    var callbackName = eventHandler.getCallbackName();
    if (channel != null) {
        args = args || {};
        args.channel = channel;
    }

    eventHandler.on(callbackName, function (context, data) {
        if (context.state == 'success') {
            if (success) { success(context, data)}
        }
        if (context.state == 'error') {
            if (failure) { failure(context, data)}
        }
    });

    swampdragon.sendJSON({
        route: route,
        verb: verb,
        args: args,
        callbackname: callbackName
    })
};


/*********************
 * Subscribe
 *********************/
swampdragon.subscribe = function(route, channel, args, success, failure) {
    return swampdragon.callRouter('subscribe', route, args, success, failure, channel);
};

swampdragon.unsubscribe = function(route, channel, args, success, failure) {
    return swampdragon.callRouter('unsubscribe', route, args, success, failure, channel);
};


/*********************
 * Get objects(s)
 *********************/
swampdragon.getSingle = function (route, data, success, failure) {
    swampdragon.callRouter('get_single', route, data, success, failure, null);
};

swampdragon.getList = function (route, data, success, failure) {
    swampdragon.callRouter('get_list', route, data, success, failure, null)
};

swampdragon.getPagedList = function (route, data, page, success, failure) {
    page = page || 1;
    data['_page'] = page;
    swampdragon.callRouter('get_list', route, data, success, failure, null)
};


/*********************
 * Create / update / delete
 *********************/
swampdragon.create = function (route, data, success, failure) {
    swampdragon.callRouter('create', route, data, success, failure, null)
};

swampdragon.update = function (route, data, success, failure) {
    swampdragon.callRouter('update', route, data, success, failure, null)
};

swampdragon["delete"] = function (route, data, success, failure) {
    swampdragon.callRouter('delete', route, data, success, failure, null)
};


module.exports = swampdragon;
