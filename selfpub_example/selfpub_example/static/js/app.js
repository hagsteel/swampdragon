var SelfPubApp = angular.module('SelfPubApp', [
    'SwampDragonServices',
    'CompanyControllers'
]);

SelfPubApp.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
