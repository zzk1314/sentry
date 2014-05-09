define([
  'angular',
  'ngBootstrap',
  'ngClassy',
  'ngHttpAuth',
  'ngLoadingBar',

  'moment',
  'jquery'
], function(angular){
  'use strict';

  return angular.module('app', [
    'classy',
    'http-auth-interceptor',
    'chieffancypants.loadingBar',
    'ui.bootstrap'
  ]);
});
