define([
  'angular'
], function(angular) {
  'use strict';

  var TEMPLATES = {
    'text': 'input-text.html'
  };

  var DEFAULT_TEMPLATE = TEMPLATES.text;

  function titleize(string) {
    string = string.replace('_', ' ');
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  angular.module('sentry.forms', [])
    .directive('formField', function() {
      return {
        restrict: 'A',
        template: '<div ng-include="fieldTemplateUrl"></div>',
        scope: {
          formField: '='
        },
        link: function(scope, element, attrs, ctrl) {
          var field = scope.formField;
          var templateName = TEMPLATES[field.type] || DEFAULT_TEMPLATE;

          if (!field.label) {
            field.label = titleize(field.name);
          }

          scope.fieldTemplateUrl = 'partials/forms/' + templateName;
          scope.field = field;
        }
      };
    });
});
