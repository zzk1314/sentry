requirejs.config({
  // TODO: we dont want this in prod
  urlArgs: "_=" + (new Date()).getTime(),
  paths: {
    'backbone': 'vendor/backbone/backbone',
    'bootstrap': 'vendor/bootstrap/dist/js/bootstrap.min',
    'bootstrap-datepicker': 'vendor/bootstrap-datepicker/js/bootstrap-datepicker',
    'd3': 'vendor/d3/d3.min',
    'd3-tip': 'vendor/d3-tip/index',
    'jquery': 'vendor/jquery/jquery.min',
    'jquery.animate-colors': 'scripts/lib/jquery.animate-colors',
    'jquery.clippy': 'scripts/lib/jquery.clippy.min',
    'jquery.cookie': 'scripts/lib/jquery.cookie',
    'jquery.flot': 'scripts/lib/jquery.flot',
    'jquery.flot.dashes': 'scripts/lib/jquery.flot.dashes',
    'jquery.flot.resize': 'scripts/lib/jquery.flot.resize',
    'jquery.flot.time': 'scripts/lib/jquery.flot.time',
    'jquery.flot.tooltip': 'scripts/lib/jquery.flot.tooltip',
    'jquery.migrate': 'scripts/lib/jquery-migrate',
    'json2': 'scripts/lib/json2',
    'moment': 'vendor/moment/moment',
    'requirejs': 'vendor/requirejs/requirejs',
    'text': 'vendor/requirejs-plugins/lib/text',
    'simple-slider': 'vendor/simple-slider/simple-slider',
    'underscore': 'vendor/underscore/underscore'
  },
  shim: {
    'backbone': {
      deps: ['json2', 'underscore']
    },
    'bootstrap': {
      deps: ['jquery']
    },
    'bootstrap-datepicker': {
      deps: ['bootstrap']
    },
    'jquery': {
      exports: ['jquery', '$']
    },
    'jquery.animate-colors': {
      deps: ['jquery']
    },
    'jquery.clippy': {
      deps: ['jquery']
    },
    'jquery.cookie': {
      deps: ['jquery']
    },
    'jquery.migrate': {
      deps: ['jquery']
    },
    'jquery.flot': {
      deps: ['jquery']
    },
    'jquery.flot.dashes': {
      deps: ['jquery.flot']
    },
    'jquery.flot.resize': {
      deps: ['jquery.flot']
    },
    'jquery.flot.time': {
      deps: ['jquery.flot']
    },
    'jquery.flot.tooltip': {
      deps: ['jquery.flot']
    },
    'simple-slider': {
      deps: ['jquery']
    },
    'underscore': {
      exports: '_'
    }
  }
});
