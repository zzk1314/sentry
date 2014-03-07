define(['app', 'angular'], function(app, angular) {
    'use strict';

    return {
        parent: 'manage_team',
        url: 'settings/',
        templateUrl: 'partials/manage-team-settings.html',
        controller: function($scope, $http, $state, selectedTeam){
            $scope.teamData = angular.copy(selectedTeam);

            // $scope.saveField = function($event) {
            //     var $element = angular.element($event.target);
            //     var $model = $element.controller('ngModel');
            //     var $name = $model.$name;
            //     var $value = $model.$modelValue;

            //     selectedTeam[$name] = $value;
            //     // TOOD: send to server
            // };

            $scope.isUnchanged = function(team) {
                return angular.equals(team, selectedTeam);
            };

            $scope.saveForm = function() {
                $http.put('/api/0/teams/' + selectedTeam.id + '/', $scope.teamData)
                    .success(function(data){
                        if (selectedTeam.slug !== data.slug) {
                            return $state.go('manage_team.settings', {
                                team_slug: data.slug
                            });
                        }

                        $scope.teamData = data;
                        angular.extend(selectedTeam, data);
                    });
            };
        }
    };
});
