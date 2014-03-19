define([
  'angular'
], function(angular) {
  'use strict';

  angular.module('sentry.eventHandlers.httpRequest', ['sentry.eventManager'])
    .run(function(EventManager){
      EventManager.registerType('http_request', {
        templateUrl: 'partials/event_handlers/http_request.html'
      });
    });
});
