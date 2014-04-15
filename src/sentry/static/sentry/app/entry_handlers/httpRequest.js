define([
  'angular'
], function(angular) {
  'use strict';

  angular.module('sentry.entryHandlers.httpRequest', ['sentry.entryManager'])
    .run(function(EntryManager){
      EntryManager.registerType('http_request', {
        title: 'HTTP Request',
        templateUrl: 'partials/entry_handlers/http_request.html'
      });
    });
});
