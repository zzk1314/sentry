define([
  'angular'
], function(angular) {
  'use strict';

  angular.module('sentry.eventHandlers.default', ['sentry.eventManager'])
    .run(function(EventManager){
      EventManager.registerType('default', {
        templateUrl: 'partials/event_handlers/default.html'
      });
    });
});
