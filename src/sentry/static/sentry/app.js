define([
  'angular',
  'ngBootstrap',
  'ngClassy',

  'moment',
  'jquery',

  'app/modules/collection'

], function(angular){
  'use strict';

  return angular.module('app', [
    'classy',
    'sentry.collection',
    'ui.bootstrap'
  ]);
});
