define(['app'], function() {
    'use strict';

    return {
        parent: 'help',
        url: 'guide/:language/',
        templateUrl: '/_static/sentry/app/templates/help-guide.html',
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
