var WithFileControllers = angular.module('WithFileControllers', ['SwampDragonServices']);

WithFileControllers.controller('WithFileCtrl', ['$scope', 'dataService', function($scope, dataService) {
    $scope.withfile = { a_bool: false };

    $scope.$on('dragonReady', function() {
//        dataService.getSingle('withfile-route', {id: 1}).then(function(data) {
//            console.log(data);
//            $scope.withfile = data;
//        }).catch(function(errors) {
//            console.log(errors);
//        })
    });

    $scope.save = function() {
        var promise = null;
        if ('id' in this.withfile) {
            promise = dataService.update('withfile-route', this.withfile);
        } else {
            promise = dataService.create('withfile-route', this.withfile);
        }

        if (promise) {
            promise.then(function(data) {
                console.log("ok");
            }).catch(function(errors) {
                console.log(errors);
            })
        }
    };

    $scope.$on("editWithFile", function (ev, wf) {
        $scope.withfile = wf;
    });

}]);


WithFileControllers.controller('WithFileListCtrl', ['$scope', 'dataService', function($scope, dataService) {
    $scope.datasource = []

    $scope.$on('dragonReady', function() {
        dataService.getList('withfile-route').then(function(data) {
            $scope.datasource = data;
        }).catch(function(errors) {
            console.log(errors);
        })
    });

    $scope.edit = function(wf) {
        $scope.$root.$broadcast("editWithFile", wf);
    }

}]);
