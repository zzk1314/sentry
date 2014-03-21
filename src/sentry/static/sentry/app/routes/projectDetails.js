define(['app', 'jquery'], function(app, $) {
    'use strict';

    return {
        parent: 'team',
        url: ':project_slug/',
        templateUrl: 'partials/project-details.html',
        abstract: true,
        controller: function(selectedProject, $scope, $stateParams){
            $scope.$parent.selectedProject = selectedProject;
        },
        resolve: {
            selectedProject: function(projectList, $q, $stateParams) {
                var deferred = $q.defer();
                var selected = $.grep(projectList, function(node){
                    return node.slug == $stateParams.project_slug;
                })[0];
                deferred.resolve(selected);
                return deferred.promise;
            }
        }
    };
});
