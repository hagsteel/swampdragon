var WithFileControllers = angular.module('WithFileControllers', []);

WithFileControllers.controller('WithFileCtrl', ['$scope', 'dataService', '$upload', function($scope, dataService, $upload) {
    $scope.withfile = {};
    $scope.progress = 0;

    $scope.updateProgress = function(progress, loaded, total) {
        $scope.progress = progress;
    };

    $scope.onFileSelect = function($files) {
        for (var i = 0; i < $files.length; i++) {
            var file = $files[i];
            $scope.upload = $upload.upload({
                url: window.swampDragon.url + '/_sdfileupload/',
                file: file
            }).progress(function(evt) {
                 $scope.progress = parseInt(100.0 * evt.loaded / evt.total);
            }).success(function(data, status, headers, config) {
                $scope.withfile.file = data.files[0];
            });
        }
    };

    $scope.save = function() {
        $scope.errors = null;
        dataService.create('withfile-route', this.withfile).then(function(data) {
            console.log(data);
        }).catch(function(response) {
            $scope.errors = response.errors;
        })
    };
}]);


WithFileControllers.controller('MultiFileCtrl', ['$scope', 'dataService', '$upload', function($scope, dataService, $upload) {
    $scope.multifile = {files: []};

    $scope.progress = 0;

    $scope.onFileSelect = function($files) {
        for (var i = 0; i < $files.length; i++) {
            var file = $files[i];
            $scope.upload = $upload.upload({
                url: window.swampDragon.url + '/_sdfileupload/',
                file: file
            }).progress(function(evt) {
                 $scope.progress = parseInt(100.0 * evt.loaded / evt.total);
            }).success(function(data, status, headers, config) {
                for (var i in data.files) {
                    $scope.multifile.files.push({file: data.files[i]});
                }
            });
        }
    };


    $scope.save = function() {
        var promise = null;
        dataService.create('multifile-route', this.multifile).then(function(data) {
        }).catch(function(errors) {
            console.log(errors);
        })
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
