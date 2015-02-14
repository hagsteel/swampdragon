var VanillaDragon = function(options) {
    options = options || {};
    var endpoint = window.swampdragon_settings.endpoint;
    var host = window.swampdragon_host;
    var sdInstance = new SwampDragon(options);

    var _dragon = {
        _callbackId: 0,

        _getCallbackName: function () {
            var callbackName = 'cb_' + this._callbackId;
            this._callbackId++;
            if (this._callbackId > 9999)
                this._callbackId = 0;
            return callbackName;
        },

        connect: function() {
            sdInstance.connect(host, endpoint)
        },

        callRouter: function (verb, route, args, success, failure, channel) {
            var _this = this;
            var callbackName = this._getCallbackName();
            sdInstance.on(callbackName, function (context, data) {
                if (context.state == 'success') {
                    if (success) { success(context, data); }
                }
                else if (context.state == 'error') {
                    if (failure) { failure(context, data); }
                } else {
                    _this._handleError(context, data, deferred);
                }
            });
            sdInstance.callRouter(verb, route, args, callbackName, channel);
        },

        getSingle: function (route, data, success, failure) {
            this.callRouter('get_single', route, data, success, failure, null);
        },

        getList: function (route, data, success, failure) {
            this.callRouter('get_list', route, data, success, failure, null)
        },

        getPagedList: function (route, data, page, success, failure) {
            page = page || 1;
            data['_page'] = page;
            this.callRouter('get_list', route, data, success, failure, null)
        },

        "create": function (route, data, success, failure) {
            this.callRouter('create', route, data, success, failure, null)
        },

        update: function (route, data, success, failure) {
            this.callRouter('update', route, data, success, failure, null)
        },

        "delete": function (route, data, success, failure) {
            this.callRouter('delete', route, data, success, failure, null)
        },

        subscribe: function (route, channel, args, success, failure) {
            this.callRouter('subscribe', route, args, success, failure, channel);
        },

        unsubscribe: function (route, channel, args, success, failure) {
            this.callRouter('unsubscribe', route, args, success, failure, channel);
        }
    };

    _dragon.connect();
    return _dragon;
};