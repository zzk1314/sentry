define(['app'], function() {
    'use strict';

    return {
        url: '/help/',
        templateUrl: '/_static/sentry/app/templates/help.html',
        controller: function(teamList, $scope){
            $scope.teamList = teamList.data;
        },
        resolve: {
            teamList: function($http, $stateParams) {
              return $http.get('/api/0/teams/');
            }
        }
    };
});
