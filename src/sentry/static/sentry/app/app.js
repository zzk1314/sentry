define([
  'angular',
  'ngBootstrap',
  'ngLoadingBar',
  'ngRoute',
  'ngRouter',
  'ngSanitize',
  'event_handlers/default',
  'event_handlers/exception',
  'event_handlers/httpRequest',
  'modules/barChart',
  'modules/eventManager',
  'modules/forms',
  'modules/simpleSlider'
  ], function (angular) {
    'use strict';

    return angular.module('app', [
      'chieffancypants.loadingBar',
      'ngRoute',
      'ngSanitize',
      'sentry.barchart',
      'sentry.eventManager',
      'sentry.eventHandlers.default',
      'sentry.eventHandlers.exception',
      'sentry.eventHandlers.httpRequest',
      'sentry.forms',
      'sentry.slider',
      'ui.bootstrap',
      'ui.router'
    ]);
});
