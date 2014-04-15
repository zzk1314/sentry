define([
  'angular'
], function(angular) {
  'use strict';

  angular.module('sentry.entryHandlers.exception', ['sentry.entryManager'])
    .run(function(EntryManager){
      EntryManager.registerType('exception', {
        title: 'Exception',
        templateUrl: 'partials/entry_handlers/exception.html'
      });
    });
});
