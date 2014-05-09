define([
  'backbone',
  'bootstrap',
  'moment',
  'jquery',

  'app/base',
  'app/core',
  'app/models',
  'app/templates',
  'app/utils',
  'app/collections',
  'app/charts',
  'app/views'
], function (Backbone, bootstrap, moment, $, appBase) {
  'use strict';

  Backbone.sync = function(method, model, success, error){
      success();
  };

  $('.clippy').clippy({
      clippy_path: '../clippy.swf',
      keep_text: true
  });

  $('input[data-toggle="datepicker"]').datepicker();

  $('.tip').tooltip({
      html: true,
      container: 'body'
  });

  $('.trigger-popover').popover({
      html: true,
      container: 'body'
  });

  $('.nav-tabs .active a').tab('show')

  $('.project-selector').on('change', function(e){
      var $el = $(e.target).get(0);
      var $opt = $($el.options[$el.selectedIndex]);
      window.location.href = $opt.attr('data-url');
      return false;
  });

  $(function(){
      // Change all select boxes to select2 elements.
      $('.body select').each(function(){
          var $this = $(this),
              options = {
                  width: 'element',
                  allowClear: false,
                  minimumResultsForSearch: 10
              };

          if ($this.attr('data-allowClear')) {
              options.allowClear = $this.attr('data-allowClear');
          }

          $this.select2(options);
      });

      // Update date strings periodically
      setInterval(function() {
          $('.pretty-date').each(function(_, el){
              var $el = $(el);
              var dt = $el.data('datetime');
              if (dt) {
                  var date = moment(dt);
                  if (date) {
                      $el.text(date.fromNow());
                      $el.attr('title', date.format('llll'));
                  }
              }
          });
      }, 5000);
  });
});
