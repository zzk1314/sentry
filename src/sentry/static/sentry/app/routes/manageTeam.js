define(['app', 'jquery'], function(app, $) {
    'use strict';

    return {
        abstract: true,
        parent: 'index',
        url: 'account/teams/:team_slug/',
        templateUrl: '/_static/sentry/app/templates/manage-team.html',
        controller: function($scope, selectedTeam){
            $scope.selectedTeam = selectedTeam;
        },
        resolve: {
            selectedTeam: function(teamList, $q, $stateParams) {
                var deferred = $q.defer();
                var selected = $.grep(teamList.data, function(node){
                    return node.slug == $stateParams.team_slug;
                })[0];
                deferred.resolve(selected);
                return deferred.promise;
            }
        }
    };
});
