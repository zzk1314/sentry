define([
  'angular'
], function(angular) {
  'use strict';

  angular.module('sentry.eventTypes.httpRequest', ['sentry.eventManager'])
    .run(function(EventManager){
      EventManager.registerType('http_request', {
        render: function(event) {
          return 'HTTP GET';
        }
      });
    });
});
