define(['app', 'angular'], function(app, angular) {
    'use strict';

    return {
        parent: 'manage_team',
        url: 'settings/',
        templateUrl: 'partials/manage-team-settings.html',
        controller: function($scope, selectedTeam){
            $scope.teamData = angular.copy(selectedTeam);

            $scope.saveField = function($event) {
                var $element = angular.element($event.target);
                var $model = $element.controller('ngModel');
                var $name = $model.$name;
                var $value = $model.$modelValue;

                selectedTeam[$name] = $value;
                // TOOD: send to server
            };
        }
    };
});
