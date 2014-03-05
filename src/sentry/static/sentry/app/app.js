define([
  'angular',
  'ngBootstrap',
  'ngLoadingBar',
  'ngRoute',
  'ngRouter',
  'ngSanitize',
  'modules/barChart'
  ], function (angular) {
    'use strict';

    return angular.module('app', [
      'chieffancypants.loadingBar',
      'ngRoute',
      'ngSanitize',
      'sentry.barchart',
      'ui.bootstrap',
      'ui.router'
    ]);
});
