var CompanyControllers = angular.module('CompanyControllers', ['SwampDragonServices']);

CompanyControllers.controller('CompanyCtrl', ['$scope', '$dragon', function($scope, $dragon) {
    $scope.channel = 'companies';
    $scope.datasource = [];

    $dragon.data.onReady(function() {
        $dragon.data.subscribe('company-route', $scope.channel, {}).then(function(response) {
            this.dataMapper = new DataMapper(response.data);
        });
        $dragon.data.getList('company-route', {}).then(function(response) {
            $scope.datasource = response.data
        });
    });

    $dragon.data.onChannelMessage(function(channels, message) {
        if (indexOf.call(channels, $scope.channel) > -1) {
            $scope.$apply(function() {
                this.dataMapper.mapData($scope.datasource, message);
            });
        }
    });

    $scope.createCompany = function() {
        $dragon.data.create('company-route', this.company).then(function(response) {
            console.log(response);
        }).catch(function(errors) {
            console.log(errors);
        });
    }
}]);
