define([
  'angular'
], function(angular) {
  'use strict';

  angular.module('sentry.eventTypes.httpRequest', ['sentry.eventManager'])
    .run(function(EventManager){
      var HttpRequestEvent = function(event){
        return {
          render: function() {
            return 'HTTP GET';
          }
        };
      };
      EventManager.registerType('http_request', HttpRequestEvent);
    });
});
