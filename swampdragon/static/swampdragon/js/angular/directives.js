var SDFileUploader = angular.module('SDFileUploader', []);

SDFileUploader.directive('sdFileUpload', ['$parse', function ($parse) {
    function link(scope, elements, attrs) {
        this.multiple = attrs.multiple;
        this.scope = scope;

        elements.change(function (e) {
            uploadFile(elements[0], attrs.route, uploadComplete);
        });

        function uploadComplete(evt) {
            var data = JSON.parse(evt.target.responseText);
            var model = $parse(attrs.ngModel);
            var model_data = $parse(attrs.ngModel + '__data');
            scope.$apply(function() {
                if (multiple) {
                    model.assign(scope, data.files);
                    model_data.assign(scope, data.files);
                } else {
                    model.assign(scope, data.files[0].file_url);
                    model_data.assign(scope, data.files[0]);
                }
            });
        }
    }

    return {
        link: link
    };
}]);
