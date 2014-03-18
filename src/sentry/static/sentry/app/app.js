define([
  'angular',
  'ngBootstrap',
  'ngLoadingBar',
  'ngRoute',
  'ngRouter',
  'ngSanitize',
  'event_types/httpRequest',
  'modules/barChart',
  'modules/eventManager',
  'modules/simpleSlider'
  ], function (angular) {
    'use strict';

    return angular.module('app', [
      'chieffancypants.loadingBar',
      'ngRoute',
      'ngSanitize',
      'sentry.barchart',
      'sentry.eventManager',
      'sentry.eventTypes.httpRequest',
      'sentry.slider',
      'ui.bootstrap',
      'ui.router'
    ]);
});
