var CompanyControllers = angular.module('CompanyControllers', ['SwampDragonServices']);

CompanyControllers.controller('CompanyCtrl', ['$scope', '$dragon', function($scope, $dragon) {
    $scope.channel = 'companies';
    $scope.datasource = [];

    $dragon.onReady(function() {
        $dragon.subscribe('company-route', $scope.channel, {}).then(function(response) {
            this.dataMapper = new DataMapper(response.data);
        });
        $dragon.getList('company-route', {}).then(function(response) {
            $scope.datasource = response.data
        });
    });

    $dragon.onChannelMessage(function(channels, message) {
        if (indexOf.call(channels, $scope.channel) > -1) {
            $scope.$apply(function() {
                this.dataMapper.mapData($scope.datasource, message);
            });
        }
    });

    $scope.createCompany = function() {
        $dragon.create('company-route', this.company).then(function(response) {
            console.log(response);
        }).catch(function(errors) {
            console.log(errors);
        });
    }
}]);
