var mainPageController = angular.module('MainPageController', []);

mainPageController.controller('MainPageController', function ($scope, Account, Goal) {
    $scope.accounts = [];
    $scope.goals = [];

    Account.query(function (data) {
        $scope.accounts = data.results;
    });

    Goal.query(function (data) {
        $scope.goals = data.results;
    });
});