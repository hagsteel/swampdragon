var CompanyControllers = angular.module('CompanyControllers', ['SwampDragonServices']);

CompanyControllers.controller('CompanyCtrl', ['$scope', 'dataService', function($scope, dataService) {
    $scope.channel = 'companies';
    $scope.datasource = [];

    $scope.$on('dragonReady', function() {
        dataService.subscribe('company-route', $scope.channel, {}).then(function(data) {
            this.dataMapper = new DataMapper(data);
        });
        dataService.get_list('company-route', {}).then(function(data) {
            $scope.datasource = data
        });
    });

    $scope.$on('handleChannelMessage', function(e, channels, message) {
        console.log(message);
        if (indexOf.call(channels, $scope.channel) > -1) {
            this.dataMapper.mapData($scope.datasource, message);
            $scope.$apply();
        }
    });
}]);
