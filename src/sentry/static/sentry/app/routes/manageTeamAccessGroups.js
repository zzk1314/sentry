define(['app'], function(app) {
    'use strict';

    return {
        parent: 'manage_team',
        url: 'access-groups/',
        templateUrl: 'partials/manage-team-access-groups.html',
        controller: function($scope, accessGroupList){
            $scope.accessGroupList = accessGroupList.data;
        },
        resolve: {
            accessGroupList: function(selectedTeam, $http) {
                return $http.get('/api/0/teams/' + selectedTeam.id + '/access-groups/');
            }
        }
    };
});
