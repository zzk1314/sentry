define([
  'angular',
  'ngBootstrap',
  'ngClassy',

  'moment',
  'jquery',

  'app/modules/charts',
  'app/modules/collection'

], function(angular){
  'use strict';

  return angular.module('app', [
    'classy',
    'sentry.charts',
    'sentry.collection',
    'ui.bootstrap'
  ]);
});
