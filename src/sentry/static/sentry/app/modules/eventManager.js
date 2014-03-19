/**
angular.module('extension.event_handlers.http_request', ['sentry.eventManager'])
  .run(function(EventManager){
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

  var EventManager = function($http){
    var _registry = {};

    var EventHandler = function(options) {
      var self = this;

      this.loading = true;

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
        var eventHandler = new EventHandler(options);

        _registry[type] = eventHandler;

        return this;
      },
      getTemplate: function(event) {
        var eventType = event.type || 'default';

        if (_registry[eventType] === undefined) {
          throw new Error('No event renderer found for type: ' + eventType);
        }

        return _registry[eventType].template;
      }
    };
  };

  angular.module('sentry.eventManager', [])
    .factory('EventManager', EventManager)
    .directive('renderEvent', function($compile, EventManager){
      return {
        restrict: 'AE',
        link: function(scope, element, attrs, ctrl) {
          scope.event = scope.$eval(attrs.renderEvent);
          element.html(EventManager.getTemplate(scope.event));
          $compile(element.contents())(scope);
        }
      };
    });
});
