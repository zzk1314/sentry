define(['app', 'jquery'], function(app, $) {
    'use strict';

    return {
        parent: 'index',
        url: ':team_slug/',
        templateUrl: '/_static/sentry/app/templates/team-details.html',
        controller: function(selectedTeam, projectList, $scope, $stateParams){
            $scope.selectedTeam = selectedTeam;
            $scope.projectList = projectList.data;
        },
        resolve: {
            selectedTeam: function(teamList, $q, $stateParams) {
                var deferred = $q.defer();
                var selected = $.grep(teamList.data, function(node){
                    return node.slug == $stateParams.team_slug;
                })[0];
                deferred.resolve(selected);
                return deferred.promise;
            },
            projectList: function(selectedTeam, $http) {
                return $http.get('/api/0/teams/' + selectedTeam.id + '/projects/');
            }
        }
    };
});
