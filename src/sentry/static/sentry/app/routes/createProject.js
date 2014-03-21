define(['angular', 'app', 'jquery'], function(angular, app, $) {
    'use strict';

    return {
        parent: 'manage_team',
        url: 'new/project/',
        templateUrl: 'partials/create-project.html',
        controller: function($scope, $http, $state, selectedTeam, userData){
            $scope.projectData = {};

            $scope.saveForm = function() {
                $http({
                    method: 'POST',
                    url: '/api/0/teams/' + selectedTeam.id + '/projects/',
                    data: angular.copy($scope.projectData)
                }).success(function(data){
                    // HACK
                    var selected = $.grep(userData.teams, function(node){
                        return node.id == selectedTeam.id;
                    })[0];
                    selected.projects.push(data);
                    $state.go('manage_team.projects');
                });
            };
        }
    };
});
