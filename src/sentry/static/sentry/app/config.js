requirejs.config({
  // TODO: we dont want this in prod
  urlArgs: "_=" + (new Date()).getTime(),
  paths: {
    'angular': '../vendor/angular/angular.min',
    'ngBootstrap': '../vendor/angular-bootstrap/ui-bootstrap-tpls',
    'ngRaven': '../vendor/angular-raven/angular-raven',
    'ngRoute': '../vendor/angular-route/angular-route',
    'ngRouter': '../vendor/angular-ui-router/release/angular-ui-router',
    'ngSanitize': '../vendor/angular-sanitize/angular-sanitize',
    'ngLoadingBar': '../vendor/angular-loading-bar/build/loading-bar',
    'd3': '../vendor/d3/d3.min',
    'd3-tip': '../vendor/d3-tip/index',
    'jquery': '../vendor/jquery/jquery.min',
    'moment': '../vendor/moment/moment',
    'requirejs': '../vendor/requirejs/requirejs',
    'simple-slider': '../vendor/simple-slider/simple-slider'
  },
  shim: {
    'angular': {
      exports: 'angular',
      deps: ['jquery']
    },
    'ngBootstrap': ['angular'],
    'ngLoadingBar': ['angular'],
    'ngRaven': ['angular'],
    'ngRoute': ['angular'],
    'ngSanitize': ['angular'],
    'ngRouter': ['angular'],
    'jquery': {
      exports: 'jquery'
    },
    'simple-slider': {
      deps: ['jquery']
    }
  }
});
