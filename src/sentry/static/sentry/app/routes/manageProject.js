define(['app', 'jquery'], function(app, $) {
    'use strict';

    return {
        abstract: true,
        parent: 'index',
        url: 'account/teams/:team_slug/projects/:project_slug/',
        templateUrl: 'partials/manage-project.html',
        controller: function($scope, $state, selectedTeam, selectedProject){
            if (!selectedProject.permission.edit) {
                // TODO(dcramer): show error message
                $state.go('index');
            }
            $scope.selectedTeam = selectedTeam;
            $scope.selectedProject = selectedProject;
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
            },
            selectedProject: function(projectList, $q, $stateParams) {
                var deferred = $q.defer();
                var selected = $.grep(projectList.data, function(node){
                    return node.slug == $stateParams.project_slug;
                })[0];
                deferred.resolve(selected);
                return deferred.promise;
            }
        }
    };
});
