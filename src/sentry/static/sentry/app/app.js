define([
  'angular',
  'ngBootstrap',
  'ngLoadingBar',
  'ngRoute',
  'ngRouter',
  'ngSanitize',
  'modules/barChart',
  'modules/simpleSlider'
  ], function (angular) {
    'use strict';

    return angular.module('app', [
      'chieffancypants.loadingBar',
      'ngRoute',
      'ngSanitize',
      'sentry.barchart',
      'sentry.slider',
      'ui.bootstrap',
      'ui.router'
    ]);
});
