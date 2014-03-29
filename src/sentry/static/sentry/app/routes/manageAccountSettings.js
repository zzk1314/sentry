define(['app', 'angular', 'jquery'], function(app, angular, $) {
    'use strict';

    return {
        parent: 'manage_account',
        url: 'settings/',
        templateUrl: 'partials/manage-account-settings.html',
        controller: function($scope, $http, $state, selectedUser){
            $scope.saveForm = function() {
                $http.put('/api/0/users/' + selectedUser.id + '/', $scope.userData)
                    .success(function(data){
                        $scope.userData = data;
                        angular.extend(selectedUser, data);
                    });
            };

            var Form = function(fields, initial){
                var field,
                    fieldName;

                this._data = angular.copy(initial || {});
                this._fields = fields;

                for (fieldName in fields) {
                    field = fields[fieldName];
                    field.name = fieldName;
                    field.value = this._data[fieldName];
                    this[fieldName] = field;
                }
            };

            Form.prototype.isUnchanged = function(){
                var data = {},
                    field,
                    fieldName;

                for (fieldName in this._fields) {
                    field = this._fields[fieldName];
                    data[fieldName] = field.value;
                }

                return angular.equals(this._data, data);
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
