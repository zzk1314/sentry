define(['angular', 'app'], function(angular, app) {
    'use strict';

    return {
        parent: 'index',
        url: 'login/',
        templateUrl: 'partials/login.html',
        controller: function($scope, $http, $state, userData){
            $scope.loginData = {};

            function addAuthHeader(data, headersGetter){
                // as per HTTP authentication spec [1], credentials must be
                // encoded in base64. Lets use window.btoa [2]
                var headers = headersGetter();
                headers.Authorization = 'Basic ' + btoa(data.username + ':' + data.password);
            }

            $scope.saveForm = function() {
                $http({
                    method: 'POST',
                    url: '/api/0/auth/login/',
                    data: angular.copy($scope.loginData),
                    transformRequest: addAuthHeader
                }).success(function(data){
                    angular.extend(userData, data);
                    // TODO(dcramer): redirect somewhere useful
                    $state.go('manage_account.settings');
                });
            };
        }
    };
});
