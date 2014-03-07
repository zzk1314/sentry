define(['app', 'jquery'], function(app, $) {
    'use strict';

    return {
        parent: 'index',
        url: ':team_slug/',
        templateUrl: 'partials/team-details.html',
        controller: function(teamList, selectedTeam, projectList, $scope){
            $scope.selectedTeam = selectedTeam;
            $scope.projectList = projectList.data;
        },
        resolve: {
            selectedTeam: function(teamList, $q, $state, $stateParams) {
                var deferred = $q.defer();
                var selected = $.grep(teamList.data, function(node){
                    return node.slug == $stateParams.team_slug;
                })[0];
                if (!selected) {
                    deferred.reject();
                    $state.go('index');
                } else {
                    deferred.resolve(selected);
                }
                return deferred.promise;
            },
            projectList: function(selectedTeam, $http) {
                return $http.get('/api/0/teams/' + selectedTeam.id + '/projects/');
            }
        }
    };
});
