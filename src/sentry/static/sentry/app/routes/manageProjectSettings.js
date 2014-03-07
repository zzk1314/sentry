define(['app', 'angular'], function(app, angular) {
    'use strict';

    return {
        parent: 'manage_project',
        url: 'settings/',
        templateUrl: 'partials/manage-project-settings.html',
        controller: function($scope, $http, $state, selectedProject, selectedTeam){
            $scope.projectData = angular.copy(selectedProject);

            $scope.isUnchanged = function(data) {
                return angular.equals(data, selectedProject);
            };

            $scope.saveForm = function() {
                $http.put('/api/0/projects/' + selectedTeam.id + '/', $scope.projectData)
                    .success(function(data){
                        if (selectedProject.slug !== data.slug) {
                            return $state.go('manage_project.settings', {
                                team_slug: selectedTeam.slug,
                                project_slug: data.slug
                            });
                        }
                        $scope.projectData = data;
                        angular.extend(selectedProject, data);
                    });
            };
        }
    };
});
