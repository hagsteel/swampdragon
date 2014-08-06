var SDFileUploader = angular.module('SDFileUploader', []);

SDFileUploader.directive('sdFileUpload', ['$parse', function ($parse) {
    return {
        link: function ($scope, elements, attrs) {
            /*
             * Allow for more than one file
             * to be uploaded
             ******************************************/
            var multiple = attrs.multiple || false;

            /*
             * Trigger file upload
             ******************************************/
            elements.change(function (e) {
                uploadFile(elements[0].files, uploadComplete, uploadProgress);
            });

            /*
             * File upload progress if such is defined on the controller
             ******************************************/
            function uploadProgress(e) {
                if ($scope[attrs.onProgress]) {
                    var progress = parseInt(100.0 * e.loaded / e.total);
                    $scope.$apply(function() { $scope[attrs.onProgress](progress, e.loaded, e.total); });
                }
            }

            /*
             * Once upload is completed, update the models
             * on the scope.
             * If "multiple" is set to true, assume the
             * parent property is the collection as multiple properties
             * with the same name can not exist
             ******************************************/
            function uploadComplete(evt) {
                console.log("done");
                var data = JSON.parse(evt.target.responseText);
                var modelNameList = attrs.ngModel.split('.');
//                var attrName = modelNameList.pop();
                var modelName = modelNameList.join('.');

                var model = $parse(modelName);
                var model_data = $parse(modelName + '__data');
                $scope.$apply(function () {
                    if (multiple) {
                        var modelFileList = model.assign($scope, []);
                        for (var i in data.files) {
                            var fileObj = {};
                            fileObj[attrName] = data.files[i];
                            modelFileList.push(fileObj);
                        }
                        model.assign($scope, modelFileList);
                        model_data.assign($scope, modelFileList);
                    } else {
                        var fileObj = {};
//                        fileObj[attrName] = data.files[0];
                        model.assign($scope, data.files[0]);
                        model_data.assign($scope, data.files[0]);
                    }
                });
            }

            /*
             * Drag'n'drop events.
             * -------------------
             * dragDropTarget should be the ID of the element
             * triggering the drop
             ******************************************/
            function dragEnterLeave(evt) {
                evt.stopPropagation();
                evt.preventDefault();
            }

            function dragOver(evt) {
                evt.stopPropagation();
                evt.preventDefault();
                var ok = evt.dataTransfer && evt.dataTransfer.types && evt.dataTransfer.types.indexOf('Files') >= 0;
            }

            function drop(evt) {
                evt.stopPropagation();
                evt.preventDefault();
                var files = evt.dataTransfer.files;
                if (files.length > 0) {
                    uploadFile(files, uploadComplete, uploadProgress);
                }
            }

            if ('dragDropTarget' in attrs) {
                this.dropTarget = document.getElementById(attrs.dragDropTarget);
                this.dropTarget.addEventListener("dragenter", dragEnterLeave, false);
                this.dropTarget.addEventListener("dragleave", dragEnterLeave, false);
                this.dropTarget.addEventListener("dragover", dragOver, false);
                dropbox.addEventListener("drop", drop, false);
            }
        }
    };
}]);
