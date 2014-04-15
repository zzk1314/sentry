define([
  'angular'
], function(angular) {
  'use strict';

  angular.module('sentry.entryHandlers.user', ['sentry.entryManager'])
    .run(function(EntryManager){
      EntryManager.registerType('user', {
        title: 'User',
        templateUrl: 'partials/entry_handlers/user.html'
      });
    });
});
