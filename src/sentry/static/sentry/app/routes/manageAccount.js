define(['app', 'angular', 'jquery'], function(app, angular, $) {
    'use strict';

    return {
        abstract: true,
        parent: 'index',
        url: 'account/',
        templateUrl: 'partials/manage-account.html',
        controller: function($scope, userData){
            $scope.userData = userData;
        },
        resolve: {
            userData: function($http) {
                return $http.get('/api/0/users/me/').then(function(response){
                    return response.data;
                });
            }
        }
    };
});
