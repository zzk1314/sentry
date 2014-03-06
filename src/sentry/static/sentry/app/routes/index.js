define(['app'], function() {
    'use strict';

    return {
        url: '/',
        templateUrl: 'partials/index.html',
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
