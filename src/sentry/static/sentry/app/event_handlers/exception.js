define([
  'angular'
], function(angular) {
  'use strict';

  angular.module('sentry.eventHandlers.exception', ['sentry.eventManager'])
    .run(function(EventManager){
      EventManager.registerType('exception', {
        templateUrl: 'partials/event_handlers/exception.html'
      });
    });
});
