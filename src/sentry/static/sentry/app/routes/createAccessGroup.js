define(['angular', 'app', 'jquery'], function(angular, app, $) {
    'use strict';

    return {
        parent: 'manage_team',
        url: 'new/access-group/',
        templateUrl: 'partials/create-access-group.html',
        controller: function($scope, $http, $state, Form, selectedTeam){
            $scope.accessGroupForm = new Form({
                name: {
                    name: 'name',
                    type: 'text',
                    placeholder: 'The Rangers'
                },
                type: {
                    name: 'type',
                    label: 'Access Type',
                    type: 'select',
                    options: [
                        {name: 'User', value: 'user'},
                        {name: 'Admin', value: 'admin'}
                    ]
                }
            });

            $scope.saveForm = function() {
                $http({
                    method: 'POST',
                    url: '/api/0/teams/' + selectedTeam.id + '/access-groups/',
                    data: $scope.accessGroupForm.getData()
                }).success(function(data){
                    $state.go('manage_team.access_groups');
                });
            };
        }
    };
});
