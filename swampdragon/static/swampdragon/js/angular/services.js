var SwampDragonServices = angular.module('SwampDragonServices', []);

SwampDragonServices.factory('dataService', ['$rootScope', '$q', function ($rootScope, $q) {
    var swampDragon = new SwampDragon({
        onchannelmessage: function (channels, data) {
            $rootScope.$broadcast('handleChannelMessage', channels, data);
        },
        onopen: function () {
            $rootScope.$broadcast('dragonReady');
        },
        onheartbeat: function() {
            $rootScope.$broadcast('heartbeat');
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

        _handleSuccess: function(context, data, deferred) {
            var response = {data: data};
            if ('client_context' in context) {
                response['context'] = context['client_context'];
            }
            deferred.resolve(response);
        },

        _handleError: function(context, data, deferred) {
            var response = {errors: data};
            deferred.reject(response);
        },

        _handleCallback: function (context, data, deferred) {
            if (context.state == 'success') {
                _this.handleSuccess(data, response);
            }
            else if (context.state == 'error') {
                _this.handleError(data, deferred);
            }
            else if (context.state == 'login_required') {
                _this.handleError(data, deferred);
                $rootScope.$broadcast('loginRequired');
            } else {
                _this.handleError(data, deferred);
            }
        },

        isReady: function() {
            return swampDragon.isReady;
        },

        on: function (eventName, callback) {
            swampDragon.on(eventName, function () {
                var args = arguments
                    callback.apply(swampDragon, args);
            });
        },

        callRouter: function (verb, route, args, channel) {
            var _this = this;
            var deferred = $q.defer();
            var callbackName = this._getCallbackName();
            swampDragon.on(callbackName, function (context, data) {
                if (context.state == 'success') {
                    _this._handleSuccess(context, data, deferred);
                }
                else if (context.state == 'error') {
                    _this._handleError(context, data, deferred);
                }
                else if (context.state == 'login_required') {
                    _this._handleError(context, data, deferred);
                    $rootScope.$broadcast('loginRequired');
                } else {
                    _this._handleError(context, data, deferred);
                }
            });
            swampDragon.callRouter(verb, route, args, callbackName, channel);
            return deferred.promise;
        },

        getList: function (route, data) {
            return this.callRouter('get_list', route, data)
        },

        getPagedList: function (route, data, page) {
            page = page || 1;
            data['_page'] = page;
            return this.callRouter('get_list', route, data)
        },

        getSingle: function (route, data) {
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
        },

        sendJSON: function(data) {
            return swampDragon.sendJSON(data);
        }
    };
}]);
