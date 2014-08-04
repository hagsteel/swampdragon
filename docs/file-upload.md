# File upload

File upload is currently only supported by:

*  Chrome 7+
*  Firefox 4+
*  IE 10+
*  Opera 12+
*  Safari 5+

Reference /static/swampdragon/js/fileupload.js

If you are using AngularJS make sure you include swampdragon/js/angular/directives.js.

## Angular
When declaring your app, include SDFileUploader.

    var FooApp = angular.module('FooApp', [
        'SDFileUploader',
        ...
    ]);

In your angular template assign the ```sd-file-uploader``` directive to your file input,
and set the model property (just like any angular model).

    <input type="file" sd-file-uploader ng-model="profile.photo">

## Upload progress

In your controller, define a function to call every time the progress is updated

    $scope.progress = 0;

    $scope.updateProgress = function(progress, loaded, total) {
        $scope.progress = progress;
    };

The function takes three arguments: 

*  progress <- The percentage done
*  loaded <- number of bytes uploaded
*  total <- total file size


## Drag'n'drop

Set the ```drag-drop-target``` attribute to the id of an element, to enable file drop on that element.

    <input type="file" sd-file-upload drag-drop-target="dropbox" ng-model="myModel.file">
