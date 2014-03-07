define(['app', 'angular', 'jquery'], function(app, angular, $) {
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
            selectedTeam: function(teamList, $q, $state, $stateParams) {
                var deferred = $q.defer();
                var selected = $.grep(teamList.data, function(node){
                    return node.slug == $stateParams.team_slug;
                })[0];
                if (!selected) {
                    // TODO(dcramer): show error message
                    deferred.reject();
                    $state.go('index');
                } else {
                    deferred.resolve(selected);
                }
                return deferred.promise;
            },
            projectList: function(selectedTeam, $http) {
                return $http.get('/api/0/teams/' + selectedTeam.id + '/projects/');
            },
            selectedProject: function(projectList, $http, $q, $state, $stateParams) {
                var deferred = $q.defer();
                var selected = $.grep(projectList.data, function(node){
                    return node.slug == $stateParams.project_slug;
                })[0];
                if (!selected) {
                    // TODO(dcramer): show error message
                    deferred.reject();
                    $state.go('index');
                } else {
                    // refresh the team data to attempt correctness
                    $http.get('/api/0/projects/' + selected.id + '/')
                        .success(function(data){
                            angular.extend(selected, data);
                            deferred.resolve(data);
                        })
                        .error(function(){
                            // TODO(dcramer): show error message
                            deferred.reject();
                            $state.go('index');
                        });
                }
                return deferred.promise;
            }
        }
    };
});
