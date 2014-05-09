require(['config'], function(config){
  'use strict';

  require([
    'angular',
    'app',
    'moment',

    'app/controllers/default',
    'app/controllers/projectStream',
    'app/controllers/teamDashboard',

    'app/directives/count',
    'app/directives/timeSince'
  ], function(angular, app, moment){
    app.config(function(
      $httpProvider, $interpolateProvider, $provide
    ) {
      // compatiblity with Django templates
      $interpolateProvider.startSymbol('<%');
      $interpolateProvider.endSymbol('%>');

      // add in Django csrf support
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

      $provide.value('config', window.SentryConfig);
    });

    moment.lang(window.SentryConfig.lang);

    angular.bootstrap(document, ['app']);
  });
});
