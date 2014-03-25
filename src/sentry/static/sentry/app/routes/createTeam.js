define(['angular', 'app'], function(angular, app) {
    'use strict';

    return {
        parent: 'manage_account',
        url: 'new/team/',
        templateUrl: 'partials/create-team.html',
        controller: function($scope, $http, $state, userData){
            $scope.teamData = {};

            $scope.saveForm = function() {
                $http({
                    method: 'POST',
                    url: '/api/0/teams/',
                    data: angular.copy($scope.teamData)
                }).success(function(data){
                    // HACK
                    userData.teams.push(data);
                    $state.go('create_project', {team_id: data.slug});
                });
            };
        }
    };
});
