define(['app', 'angular', 'jquery'], function(app, angular, $) {
    'use strict';

    return {
        abstract: true,
        parent: 'index',
        url: 'account/teams/:team_slug/',
        templateUrl: 'partials/manage-team.html',
        controller: function($scope, $state, selectedTeam){
            if (!selectedTeam.permission.edit) {
                // TODO(dcramer): show error message
                $state.go('index');
            }
            $scope.selectedTeam = selectedTeam;
        },
        resolve: {
            selectedTeam: function(teamList, $http, $q, $state, $stateParams) {
                var deferred = $q.defer();
                var selected = $.grep(teamList.data, function(node){
                    return node.slug == $stateParams.team_slug;
                })[0];
                if (!selected) {
                    // TODO(dcramer): show error message
                    deferred.reject();
                    $state.go('index');
                } else {
                    // refresh the team data to attempt correctness
                    $http.get('/api/0/teams/' + selected.id + '/')
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
