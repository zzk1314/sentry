define(['app'], function(app) {
    'use strict';

    return {
        parent: 'manage_team',
        url: 'members/',
        templateUrl: 'partials/manage-team-members.html',
        controller: function($scope, memberList){
            $scope.memberList = memberList;
        },
        resolve: {
            memberList: function(selectedTeam, $http) {
                return $http.get('/api/0/teams/' + selectedTeam.id + '/members/').then(function(response){
                    return response.data;
                });
            }
        }
    };
});
