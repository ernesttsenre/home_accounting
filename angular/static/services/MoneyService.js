var moneyService = angular.module('MoneyService', ['ngResource'])

moneyService.factory("Account", function ($resource) {
    return $resource("/api/accounts/:id", {}, {
        query: {
            method: 'GET',
            isArray: false
        }
    });
});

moneyService.factory("Goal", function ($resource) {
    return $resource("/api/goals/:id", {}, {
        query: {
            method: 'GET',
            isArray: false
        }
    });
});