var SDFileUploader = angular.module('SDFileUploader', []);

SDFileUploader.directive('sdFileUpload', ['$parse', function ($parse) {
    return {
        link: function(scope, elements, attrs) {
            this.multiple = attrs.multiple;
            this.scope = scope;

            elements.change(function (e) {
                uploadFile(elements[0], attrs.route, uploadComplete);
            });

            function uploadComplete(evt) {
                var data = JSON.parse(evt.target.responseText);
                var modelNameList = attrs.ngModel.split('.');
                var attrName = modelNameList.pop();
                var modelName = modelNameList.join('.');

                var model = $parse(modelName);
                var model_data = $parse(modelName + '__data');
                scope.$apply(function() {
                    if (multiple) {
                        var modelFileList = model.assign(scope, []);
                        for (var i in data.files) {
                            var fileObj = {};
                            fileObj[attrName] = data.files[i];
                            modelFileList.push(fileObj);
                        }
                        model.assign(scope, modelFileList);
                        model_data.assign(scope, modelFileList);
                    } else {
                        model.assign(scope, data.files[0].file_url);
                        model_data.assign(scope, data.files[0]);
                    }
                });
            }
        }
    };
}]);
