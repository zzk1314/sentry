define(['app'], function() {
    'use strict';

    return {
        url: '/',
        templateUrl: 'partials/index.html',
        controller: function(userData, teamList, $scope){
            $scope.userData = userData.data;
            $scope.teamList = teamList.data;
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
