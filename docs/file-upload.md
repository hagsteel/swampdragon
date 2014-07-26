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

In your angular template assign the ```sd-file-uploader``` directive on your file input,
and set the route attribute to the route you are calling.

    <input type="file" sd-file-uploader route="accounts" ng-model="profile.photo">

