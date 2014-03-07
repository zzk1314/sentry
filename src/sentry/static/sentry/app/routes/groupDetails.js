define(['app'], function(app) {
    'use strict';

    return {
        parent: 'project',
        url: 'group/:group_id/',
        templateUrl: 'partials/group-details.html',
        controller: function($http, $scope, $stateParams, groupData, selectedEvent){
            $scope.selectedGroup = groupData.data;
            $scope.selectedEvent = selectedEvent.data;

            $scope.chartNumDays = 1;

            $scope.$watch('chartNumDays', function(num){
                var url = '/api/0/groups/' + $stateParams.group_id + '/stats/?days=' + num;
                $http.get(url)
                    .success(function(data){
                        $scope.historicalGroupData = data;
                    });
            });
        },
        resolve: {
            groupData: function($http, $stateParams) {
                return $http.get('/api/0/groups/' + $stateParams.group_id + '/');
            },
            selectedEvent: function($http, $stateParams) {
                return $http.get('/api/0/groups/' + $stateParams.group_id + '/events/latest/');
            }
        }
    };
});
