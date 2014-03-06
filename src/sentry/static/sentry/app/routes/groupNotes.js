define(['app'], function(app) {
    'use strict';

    return {
        parent: 'group',
        url: 'notes/',
        templateUrl: 'partials/group-notes.html',
        controller: function($scope, noteList){
            $scope.noteList = noteList;
        },
        resolve: {
            noteList: function($http, $stateParams) {
                return $http.get('/api/0/groups/' + $stateParams.group_id + '/notes/');
            }
        }
    };
});
