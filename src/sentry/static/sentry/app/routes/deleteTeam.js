define(['app'], function(app) {
    'use strict';

    return {
        parent: 'manage_team',
        url: 'remove/',
        templateUrl: 'partials/delete-team.html',
        controller: function($scope, $http, selectedTeam, projectList){
            $scope.saveForm = function() {
                $http({
                    method: 'DELETE',
                    url: '/api/0/teams/' + selectedTeam.id + '/'
                }).success(function(data){
                    // TODO(dcramer): redirect + show flash message
                });
            };
            $scope.projectList = projectList;
        },
        resolve: {
            projectList: function($http, selectedTeam) {
                return $http.get('/api/0/teams/' + selectedTeam.id + '/projects/').then(function(response){
                    return response.data;
                });
            }
        }
    };
});
