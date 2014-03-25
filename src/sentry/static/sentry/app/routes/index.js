define(['app'], function() {
    'use strict';

    return {
        url: '/',
        templateUrl: 'partials/index.html',
        controller: function(userData, teamList, $state, $scope){
            $scope.userData = userData;
            $scope.teamList = teamList;
            if (teamList.length === 0) {
                $state.go('create_team', {}, {location: false});
            }
        },
        resolve: {
            userData: function($http) {
                return $http.get('/api/0/users/me/').then(function(response){
                    return response.data;
                });
            },
            teamList: function($state, userData) {
                return userData.teams;
            }
        }
    };
});
