define([
  'angular'
], function(angular) {
  'use strict';

  angular.module('sentry.entryHandlers.default', ['sentry.entryManager'])
    .run(function(EntryManager){
      EntryManager.registerType('default', {
        title: 'Entry',
        templateUrl: 'partials/entry_handlers/default.html'
      });
    });
});
