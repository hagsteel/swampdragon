var ChatControllers = angular.module('ChatControllers', []);

ChatControllers.controller('ChatCtrl', ['$scope', '$dragon', function($scope, $dragon) {
    $scope.channel = 'chat';
    $scope.messages = [];

    /// Subscribe to the chat router
    $dragon.onReady(function() {
        $dragon.subscribe('chat-route', $scope.channel).then(function(response) {
        });
    });

    $dragon.onChannelMessage(function(channels, message) {
        if (indexOf.call(channels, $scope.channel) > -1) {
            $scope.$apply(function() {
                $scope.messages.unshift(message);
            });
        }
    });

    $scope.sendMessage = function() {
        $scope.errors = null;
        $dragon.callRouter('chat', 'chat-route', {message: this.message, name: this.name})
            .then(function(response) {
                $scope.message = '';
            })
            ["catch"](function(response) {
                $scope.errors = response.errors;
            });
    }
}]);
