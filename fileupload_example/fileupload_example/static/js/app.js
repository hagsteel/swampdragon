var WithFileApp = angular.module('WithFileApp', [
    'SwampDragonServices',
    'SDFileUploader',
    'WithFileControllers'
]);

WithFileApp.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
