define(['app'], function() {
    'use strict';

    return {
        url: '/',
        templateUrl: 'partials/index.html',
        controller: function(userData, teamList, $state, $scope){
            $scope.userData = userData.data;
            $scope.teamList = teamList.data;
            // TODO(dcramer): figure out how to do this without always forcing it
            // if ($scope.teamList.length == 1) {
            //     $state.go('team', {team_slug: $scope.teamList[0].slug});
            // }
        },
        resolve: {
            userData: function($http) {
                return $http.get('/api/0/users/me/');
            },
            teamList: function(userData) {
                return {data: userData.data.teams};
            }
        }
    };
});
