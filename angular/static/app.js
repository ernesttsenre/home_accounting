var app = angular.module('project', ['Controllers', 'ngRoute']);

app.config(
    ['$interpolateProvider', '$routeProvider', function ($interpolateProvider, $routeProvider) {
        // Настройка тегов
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');

        // Настройка роутеров
        $routeProvider.
            when('/', {
                templateUrl: '/static/templates/main_page.html',
                controller: 'MainPageController'
            }).
            when('/account/:id', {
                templateUrl: '/static/templates/account_detail.html',
                controller: 'AccountController'
            }).
            when('/', {
                templateUrl: '/static/templates/main_page.html',
                controller: 'MainPageController'
            }).
            otherwise({
                redirectTo: '/'
            });
    }]
);