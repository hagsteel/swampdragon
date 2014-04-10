var WithFileControllers = angular.module('WithFileControllers', ['SwampDragonServices']);

WithFileControllers.controller('WithFileCtrl', ['$scope', 'dataService', function($scope, dataService) {
    $scope.withfile = {
        name: 'test',
        created: '23/12/2014 10:02:23',
        a_bool: true
    };
    $scope.$on('dragonReady', function() {
        $scope.save = function() {
            dataService.create('withfile-route', this.withfile).then(function(data) {
                console.log("ok");
            }).catch(function(errors) {
                console.log(errors);
            })
        };
    });
}]);
