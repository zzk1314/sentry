define(['app'], function() {
    'use strict';

    return {
        parent: 'group',
        url: 'event/:event_id/',
        templateUrl: '/_static/sentry/app/templates/event-details.html',
        controller: function($scope, selectedEvent){
            $scope.$parent.selectedEvent = selectedEvent.data;
        },
        resolve: {
            selectedEvent: function($http, $stateParams) {
                return $http.get('/api/0/events/' + $stateParams.event_id + '/');
            }
        }
    };
});
