define(['app'], function(app) {
    'use strict';

    return {
        parent: 'manage_team',
        url: 'projects/',
        templateUrl: '/_static/sentry/app/templates/manage-team-projects.html',
        controller: function($scope, projectList){
            $scope.projectList = projectList.data;
        },
        resolve: {
            projectList: function(selectedTeam, $http) {
                return $http.get('/api/0/teams/' + selectedTeam.id + '/projects/');
            }
        }
    };
});
