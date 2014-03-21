define(['app'], function() {
    'use strict';

    return {
        url: '/',
        templateUrl: 'partials/index.html',
        controller: function(userData, teamList, $state, $scope){
            $scope.userData = userData;
            $scope.teamList = teamList;
            // TODO(dcramer): figure out how to do this without always forcing it
            // if ($scope.teamList.length == 1) {
            //     $state.go('team', {team_slug: $scope.teamList[0].slug});
            // }
        },
        resolve: {
            userData: function($http) {
                return $http.get('/api/0/users/me/').then(function(response){
                    return response.data;
                });
            },
            teamList: function(userData) {
                return userData.teams;
            }
        }
    };
});
