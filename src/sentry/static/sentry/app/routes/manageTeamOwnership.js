define(['app', 'angular'], function(app, angular) {
    'use strict';

    return {
        parent: 'manage_team',
        url: 'transfer-ownership/',
        templateUrl: 'partials/manage-team-ownership.html',
        controller: function($scope, $http, selectedTeam){
            $scope.newOwner = null;

            $scope.isUnchanged = function(value) {
                return value === null;
            };

            $scope.saveForm = function() {
                $http.put('/api/0/teams/' + selectedTeam.id + '/', {
                    'owner': $scope.newOwner
                }).success(function(data){
                    angular.extend(selectedTeam, data);
                    $scope.newOwner = null;
                    // TODO(dcramer): redirect + show flash message
                });
            };
        }
    };
});
