var SDFileUploader = angular.module('SDFileUploader', []);

SDFileUploader.directive('sdFileUpload', ['$parse', function ($parse) {
    return {
        link: function (scope, elements, attrs) {
            var multiple = attrs.multiple || false;
            this.scope = scope;

            elements.change(function (e) {
                uploadFile(elements[0], uploadComplete, uploadProgress);
            });

            function uploadProgress(e) {
                var progress = parseInt(100.0 * e.loaded / e.total);
                console.log(progress);
            }

            function uploadComplete(evt) {
                var data = JSON.parse(evt.target.responseText);
                var modelNameList = attrs.ngModel.split('.');
                var attrName = modelNameList.pop();
                var modelName = modelNameList.join('.');

                var model = $parse(modelName);
                var model_data = $parse(modelName + '__data');
                scope.$apply(function () {
                    var fileObj = {};
                    if (multiple) {
                        var modelFileList = model.assign(scope, []);
                        for (var i in data.files) {
                            fileObj[attrName] = data.files[i];
                            modelFileList.push(fileObj);
                        }
                        model.assign(scope, modelFileList);
                        model_data.assign(scope, modelFileList);
                    } else {
                        fileObj[attrName] = data.files[0];
                        model.assign(scope, fileObj);
                        model_data.assign(scope, fileObj);
                    }
                });
            }
        }
    };
}]);
