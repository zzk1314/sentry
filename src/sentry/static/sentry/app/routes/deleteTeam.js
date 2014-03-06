define(['app'], function(app) {
    'use strict';

    return {
        parent: 'manage_team',
        url: 'remove/',
        templateUrl: 'partials/delete-team.html',
        controller: function($scope, $http, selectedTeam){
            $scope.saveForm = function() {
                $http({
                    method: 'DELETE',
                    url: '/api/0/teams/' + selectedTeam.id + '/'
                }).success(function(data){
                    // TODO(dcramer): redirect + show flash message
                });
            };
        }
    };
});
