define(['app'], function() {
    'use strict';

    return {
        parent: 'project',
        url: 'stream/',
        templateUrl: 'partials/project-stream.html',
        controller: function($scope, groupList){
            $scope.groupList = groupList.data;
        },
        resolve: {
            groupList: function(selectedProject, $http, $stateParams) {
              return $http.get('/api/0/projects/' + selectedProject.id + '/groups/');
            }
        }
    };
});
