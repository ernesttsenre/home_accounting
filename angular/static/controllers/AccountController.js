var accountController = angular.module('AccountController', []);

accountController.controller('AccountController', function ($scope, Account) {
    Account.get({ id: $scope.id }, function (data) {
        $scope.accounts = data.results;
    });
});