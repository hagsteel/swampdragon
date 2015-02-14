var SwampDragonServices = angular.module('SwampDragonServices', []);


SwampDragonServices.factory('$dragon', ['$q', '$timeout', function ($q, $timeout) {
    return {
        callRouter: function (verb, route, args, channel) {
            var _this = this;
            var deferred = $q.defer();
            swampdragon.callRouter(verb, route, args, function (context, data) {
                var response = {data: data};
                if ('client_context' in context) {
                    response['context'] = context['client_context'];
                }
                deferred.resolve(response);
            }, function (context, data) {
                var response = {errors: data};
                deferred.reject(response);
            }, channel );

            return deferred.promise;
        },

        onChannelMessage: swampdragon.onChannelMessage,
        onReady: swampdragon.ready,

        getList: function (route, data) {
            return this.callRouter('get_list', route, data);
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
        }
    };
}]);

