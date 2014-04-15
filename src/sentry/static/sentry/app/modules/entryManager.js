/**
angular.module('extension.entry_handlers.http_request', ['sentry.entryManager'])
  .run(function(EntryManager){
    var HttpRequestType = function(){
      return {
        renderEvent: function(event) {
          return '';
        }
      }
    }
    EventManager.registerType('http_request', HttpRequestType);
  });
*/

define([
  'angular'
], function(angular) {
  'use strict';

  var EntryManager = function($http){
    var _registry = {};

    var EntryHandler = function(options) {
      var self = this;

      this.loading = true;

      this.title = options.title;

      if (options.templateUrl) {
        $http.get(options.templateUrl, {cache: true}).success(function(data){
          self.template = data;
          self.loading = false;
        });
      } else {
        this.template = options.template;
        this.loading = false;
      }

      if (options.render) {
        this.render = options.render;
      }
    };

    return {
      registerType: function(type, options) {
        var handler = new EntryHandler(options);

        _registry[type] = handler;

        return this;
      },
      getHandler: function(entry) {
        var type = entry.type || 'default';

        if (_registry[type] === undefined) {
          throw new Error('No handler found for entry type: ' + type);
        }
        return _registry[type];
      },
      getTitle: function(entry) {
        return this.getHandler(entry).title;
      },
      getTemplate: function(entry) {
        return this.getHandler(entry).template;
      }
    };
  };

  angular.module('sentry.entryManager', [])
    .factory('EntryManager', EntryManager)
    .directive('renderEntryBody', function($compile, EntryManager){
      return {
        restrict: 'AE',
        link: function(scope, element, attrs, ctrl) {
          var entry = scope.$eval(attrs.renderEntryBody);
          element.html(EntryManager.getTemplate(entry));

          scope.data = entry.data;

          $compile(element.contents())(scope);
        }
      };
    })
    .directive('renderEntryTitle', function($compile, EntryManager){
      return {
        restrict: 'AE',
        link: function(scope, element, attrs, ctrl) {
          var entry = scope.$eval(attrs.renderEntryTitle);

          element.text(EntryManager.getTitle(entry));
        }
      };
    });
});
