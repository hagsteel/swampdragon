var WithFileControllers = angular.module('WithFileControllers', ['SwampDragonServices']);

WithFileControllers.controller('WithFileCtrl', ['$scope', 'dataService', function($scope, dataService) {
    $scope.withfile = { a_bool: false };
    $scope.progress = 0;

    $scope.updateProgress = function(progress, loaded, total) {
        $scope.progress = progress;
    };

    $scope.save = function() {
        var promise = null;
        if ('id' in this.withfile) {
            promise = dataService.update('withfile-route', this.withfile);
        } else {
            promise = dataService.create('withfile-route', this.withfile);
        }

        if (promise) {
            promise.then(function(data) {

            }).catch(function(errors) {
                console.log(errors);
            })
        }
    };
}]);


WithFileControllers.controller('MultiFileCtrl', ['$scope', 'dataService', function($scope, dataService) {
    $scope.multifile = {};

    $scope.progress = 0;

    $scope.updateProgress = function(progress, loaded, total) {
        $scope.progress = progress;
    };


    $scope.save = function() {
        var promise = null;
        if ('id' in this.multifile) {
            promise = dataService.update('multifile-route', this.multifile);
        } else {
            console.log(this.multifile);
            promise = dataService.create('multifile-route', this.multifile);
        }

        if (promise) {
            promise.then(function(data) {

            }).catch(function(errors) {
                console.log(errors);
            })
        }
    };
}]);


WithFileControllers.controller('WithFileListCtrl', ['$scope', 'dataService', function($scope, dataService) {
    $scope.datasource = [];

    $scope.$on('dragonReady', function() {
        dataService.getList('withfile-route').then(function(response) {
            $scope.datasource = response.data;
        }).catch(function(response) {
            console.log(response.errors);
        })
    });
}]);


WithFileControllers.controller('MultiFileListCtrl', ['$scope', 'dataService', function($scope, dataService) {
    $scope.datasource = [];

    $scope.$on('dragonReady', function() {
        dataService.getList('multifile-route').then(function(response) {
            $scope.datasource = response.data;
        }).catch(function(response) {
            console.log(response.errors);
        })
    });
}]);
