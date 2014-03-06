define(['app'], function(app) {
    'use strict';

    return {
        parent: 'manage_project',
        url: 'remove/',
        templateUrl: 'partials/delete-project.html',
        controller: function($scope, $http, selectedProject){
            $scope.saveForm = function() {
                $http({
                    method: 'DELETE',
                    url: '/api/0/projects/' + selectedProject.id + '/'
                }).success(function(data){
                    // TODO(dcramer): redirect + show flash message
                });
            };
        }
    };
});
