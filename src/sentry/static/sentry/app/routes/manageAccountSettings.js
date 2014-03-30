define(['app', 'angular', 'jquery'], function(app, angular, $) {
    'use strict';

    return {
        parent: 'manage_account',
        url: 'settings/',
        templateUrl: 'partials/manage-account-settings.html',
        controller: function($scope, $http, $state, selectedUser, Form){
            $scope.saveForm = function() {
                $http.put('/api/0/users/' + selectedUser.id + '/', $scope.settingsForm.getData())
                    .success(function(data){
                        $scope.settingsForm.setData(data);
                        angular.extend(selectedUser, data);
                    });
            };

            $scope.settingsForm = new Form({
                name: {
                    name: 'name',
                    type: 'text',
                    placeholder: 'Walter White'
                },
                email: {
                    name: 'email',
                    type: 'email',
                    placeholder: 'walter.white@example.com'
                }
            }, selectedUser);
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
