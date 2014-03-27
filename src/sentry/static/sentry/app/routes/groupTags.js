define(['app'], function(app) {
    'use strict';

    return {
        parent: 'group',
        url: 'tags/',
        templateUrl: 'partials/group-tags.html',
        controller: function($scope, tagList){
            $scope.tagList = tagList;
        },
        resolve: {
            tagList: function($http, $stateParams) {
                return $http.get('/api/0/groups/' + $stateParams.group_id + '/tags/').then(function(response){
                    return response.data;
                });
            }
        }
    };
});
