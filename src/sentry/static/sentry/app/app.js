define([
  'angular',
  'ngBootstrap',
  'ngHttpAuth',
  'ngLoadingBar',
  'ngRoute',
  'ngRouter',
  'ngSanitize',
  'entry_handlers/default',
  'entry_handlers/exception',
  'entry_handlers/httpRequest',
  'entry_handlers/user',
  'modules/auth',
  'modules/barChart',
  'modules/entryManager',
  'modules/forms',
  'modules/simpleSlider'
  ], function (angular) {
    'use strict';

    return angular.module('app', [
      'http-auth-interceptor',
      'chieffancypants.loadingBar',
      'ngRoute',
      'ngSanitize',
      'sentry.auth',
      'sentry.barchart',
      'sentry.entryManager',
      'sentry.entryHandlers.default',
      'sentry.entryHandlers.exception',
      'sentry.entryHandlers.httpRequest',
      'sentry.entryHandlers.user',
      'sentry.forms',
      'sentry.slider',
      'ui.bootstrap',
      'ui.router'
    ]);
});
