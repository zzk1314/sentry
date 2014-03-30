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
    .factory('Form', function() {
      var Form = function(fields, initial){
        var field,
            fieldName;

        this._data = angular.copy(initial || {});
        this._fields = fields;

        for (fieldName in fields) {
          field = fields[fieldName];
          field.name = fieldName;
          field.value = this._data[fieldName];
          this[fieldName] = field;
        }
      };

      Form.prototype.isUnchanged = function(){
        var data = {},
            field,
            fieldName;

        for (fieldName in this._fields) {
          field = this._fields[fieldName];
          data[fieldName] = field.value;
        }

        return angular.equals(this._data, data);
      };

      Form.prototype.getData = function(){
        return this._data;
      };

      Form.prototype.setData = function(data){
        this._data = data;
      };

      return Form;
    })
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
