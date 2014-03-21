define(['app', 'angular', 'jquery'], function(app, angular, $) {
    'use strict';

    return {
        parent: 'manage_account',
        url: 'settings/',
        templateUrl: 'partials/manage-account-settings.html',
        controller: function($scope, $http, $state, selectedUser){
            $scope.userData = angular.copy(selectedUser);

            $scope.isUnchanged = function(data) {
                return angular.equals(data, selectedUser);
            };

            $scope.saveForm = function() {
                $http.put('/api/0/users/' + selectedUser.id + '/', $scope.userData)
                    .success(function(data){
                        $scope.userData = data;
                        angular.extend(selectedUser, data);
                    });
            };
        },
        resolve: {
            selectedUser: function($http) {
                return $http.get('/api/0/users/me/').then(function(response){
                    return response.data;
                });
            }
        }
    };
});
