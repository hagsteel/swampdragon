var WithFileApp = angular.module('WithFileApp', [
    'SwampDragonServices',
    'angularFileUpload',
    'WithFileControllers'
]);

WithFileApp.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
