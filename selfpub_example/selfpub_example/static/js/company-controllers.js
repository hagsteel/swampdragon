var CompanyControllers = angular.module('CompanyControllers', ['SwampDragonServices']);

CompanyControllers.controller('CompanyCtrl', ['$scope', 'dataService', function($scope, dataService) {
    $scope.channel = 'companies';
    $scope.datasource = [];

    $scope.$on('dragonReady', function() {
        dataService.subscribe('company-route', $scope.channel, {}).then(function(response) {
            this.dataMapper = new DataMapper(response.data);
        });
        dataService.getList('company-route', {}).then(function(response) {
            $scope.datasource = response.data
        });
    });

    $scope.$on('handleChannelMessage', function(e, channels, message) {
        console.log(message);
        if (indexOf.call(channels, $scope.channel) > -1) {
            $scope.$apply(function() {
                this.dataMapper.mapData($scope.datasource, message);
            });
        }
    });

    $scope.createCompany = function() {
        dataService.create('company-route', this.company).then(function(response) {
            console.log(response);
        }).catch(function(errors) {
            console.log(errors);
        });
    }
}]);
