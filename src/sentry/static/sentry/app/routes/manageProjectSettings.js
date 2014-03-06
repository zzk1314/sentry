define(['app', 'angular'], function(app, angular) {
    'use strict';

    return {
        parent: 'manage_project',
        url: 'settings/',
        templateUrl: 'partials/manage-project-settings.html',
        controller: function($scope, $http, selectedProject){
            $scope.projectData = angular.copy(selectedProject);

            $scope.isUnchanged = function(data) {
                return angular.equals(data, selectedProject);
            };

            $scope.saveForm = function() {
                $http.put('/api/0/projects/' + $scope.projectData.id + '/', $scope.projectData)
                    .success(function(data){
                        $scope.projectData = data;
                        angular.extend(selectedProject, data);
                    });
            };
        }
    };
});
