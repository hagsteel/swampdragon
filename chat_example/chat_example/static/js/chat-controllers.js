var ChatControllers = angular.module('ChatControllers', ['SwampDragonServices']);

ChatControllers.controller('ChatCtrl', ['$scope', 'dataService', function($scope, dataService) {
    $scope.channel = 'chat';
    $scope.messages = [];

    $scope.$on('dragonReady', function() {
        dataService.subscribe('chat-route', $scope.channel, {});
    });

    $scope.$on('handleChannelMessage', function(e, channels, message) {
        if (indexOf.call(channels, $scope.channel) > -1) {
            $scope.messages.unshift(message);
            $scope.$apply();
        }
    });

    $scope.sendMessage = function() {
        $scope.errors = null;
        dataService.callRouter('chat', 'chat-route', {message: this.message, name: this.name})
            .then(function(data) { })
            .catch(function(errors) {
                $scope.errors = errors;
            });
    }
}]);
