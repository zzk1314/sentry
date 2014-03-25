define(['app', 'angular', 'jquery'], function(app, angular, $) {
    'use strict';

    return {
        parent: 'manage_account',
        url: 'teams/',
        templateUrl: 'partials/manage-account-teams.html',
        controller: function($scope, teamList){
            $scope.teamList = teamList;
        },
        resolve: {
            teamList: function($http) {
                return $http.get('/api/0/teams/').then(function(response){
                    return response.data;
                });
            }
        }
    };
});
