var SwampDragonServices = angular.module('SwampDragonServices', []);

SwampDragonServices.factory('dataService', ['$rootScope', '$q', function ($rootScope, $q) {
    var swampDragon = new SwampDragon({
        onchannelmessage: function (channels, data) {
            $rootScope.$broadcast('handleChannelMessage', channels, data);
        },
        onopen: function () {
            $rootScope.$broadcast('dragonReady');
        }
    });

    swampDragon.connect('http://' + window.location.hostname + ':9999', 'data');

    return {
        _callbackId: 0,

        _getCallbackName: function () {
            var callbackName = 'cb_' + this._callbackId;
            this._callbackId++;
            if (this._callbackId > 9999)
                this._callbackId = 0;
            return callbackName;
        },

        _handleCallback: function (context, data, deferred) {
            if (context.state == 'success')
                deferred.resolve(data);
            else if (context.state == 'error')
                deferred.reject(data);
            else if (context.state == 'login_required')
                console.log("LOGIN REQUIRED");
            deferred.reject(data);
        },

        on: function (eventName, callback) {
            swampDragon.on(eventName, function () {
                var args = arguments
                $rootScope.$apply(function () {
                    callback.apply(swampDragon, args);
                });
            });
        },

        callRouter: function (verb, route, args, channel) {
            var _this = this;
            var deferred = $q.defer()
            var callbackName = this._getCallbackName()
            swampDragon.on(callbackName, function (context, data) {
                _this._handleCallback(context, data, deferred);
            });
            swampDragon.callRouter(verb, route, args, callbackName, channel);
            return deferred.promise;
        },

        get_list: function (route, data) {
            return this.callRouter('get_list', route, data)
        },

        get_single: function (route, data) {
            return this.callRouter('get_single', route, data)
        },

        create: function (route, data) {
            return this.callRouter('create', route, data)
        },

        update: function (route, data) {
            return this.callRouter('update', route, data)
        },

        "delete": function (route, data) {
            return this.callRouter('delete', route, data)
        },

        subscribe: function (route, channel, args) {
            return this.callRouter('subscribe', route, args, channel);
        },

        unsubscribe: function (route, channel, args) {
            return this.callRouter('unsubscribe', route, args, channel);
        }
    };
}]);
