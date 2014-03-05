define(['app', 'jquery'], function(app, $) {
    'use strict';

    return {
        parent: 'team',
        url: ':project_slug/',
        templateUrl: '/_static/sentry/app/templates/project-details.html',
        abstract: true,
        controller: function(selectedProject, $scope, $stateParams){
            $scope.selectedProject = selectedProject;
        },
        resolve: {
            selectedProject: function(projectList, $q, $stateParams) {
                var deferred = $q.defer();
                var selected = $.grep(projectList.data, function(node){
                    return node.slug == $stateParams.project_slug;
                })[0];
                deferred.resolve(selected);
                return deferred.promise;
            }
        }
    };
});
