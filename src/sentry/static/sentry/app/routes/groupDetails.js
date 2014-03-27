define(['app'], function(app) {
    'use strict';

    return {
        parent: 'project',
        url: 'group/:group_id/',
        templateUrl: 'partials/group-details.html',
        controller: function($http, $scope, $state, $stateParams, groupData){
            $scope.selectedGroup = groupData;
            $scope.selectedEvent = null;

            $scope.chartNumDays = 1;

            $scope.$watch('chartNumDays', function(num){
                var url = '/api/0/groups/' + $stateParams.group_id + '/stats/?days=' + num;
                $http.get(url)
                    .success(function(data){
                        $scope.historicalGroupData = data;
                    });
            });

            if ($state.current.name == 'group') {
                $state.go('event', {event_id: 'latest'}, {location: false});
            }
        },
        resolve: {
            groupData: function($http, $stateParams) {
                return $http.get('/api/0/groups/' + $stateParams.group_id + '/').then(function(response){
                    return response.data;
                });
            }
        }
    };
});
