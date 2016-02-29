var nttApp = angular.module('nttApp', [
    'ngRoute',
    'ngCookies',
    'http-auth-interceptor',
]);

nttApp.config(['$httpProvider', '$interpolateProvider', function($httpProvider, $interpolateProvider){
    /* For compatibility with django template engine */
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    /* Adding XMLHttpRequest to angular AJAX request */
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

    /* CSRF Protection */
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

nttApp.config(['$routeProvider', function($routeProvider){
    $routeProvider.when('/', {
        controller: 'IndexCtrl',
        templateUrl: '/static/partials/index.html',
    });

    $routeProvider.when('/dashboard/', {
        controller: 'DashboardCtrl',
        templateUrl: '/static/partials/dashboard.html',
    });

    $routeProvider.when('/clouds/', {
        controller: 'CloudsCtrl',
        templateUrl: '/static/partials/cloud/clouds.html',
    });

    $routeProvider.when('/cloud/:cloudId/', {
        controller: 'CloudCtrl',
        templateUrl: '/static/partials/cloud/cloud_view.html',
    });

    $routeProvider.when('/clouds/:event/', {
        controller: 'CloudCtrl',
        templateUrl: '/static/partials/cloud/cloud.html',
    });

    $routeProvider.when('/clouds/:event/:cloudId/', {
        controller: 'CloudCtrl',
        templateUrl: '/static/partials/cloud/cloud.html',
    });

    $routeProvider.when('/cloudtraffic/add/:cloudId/', {
        controller: 'CloudTrafficCtrl',
        templateUrl: '/static/partials/cloud/cloudtraffic_form.html',
    });

    $routeProvider.when('/cloudtraffic/view/:id/', {
        controller: 'CloudTrafficViewCtrl',
        templateUrl: '/static/partials/cloud/cloudtraffic_view.html',
    });

    $routeProvider.when('/cloudtraffictest/', {
        controller: 'CloudTrafficTestCtrl',
        templateUrl: '/static/partials/cloud/cloudtraffic_test.html'
    });
}]);


