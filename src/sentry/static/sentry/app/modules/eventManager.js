/**
angular.module('extension.types.http_request', ['sentry.eventManager'])
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

  var EventManager = function($compile, $http){
    var _registry = {};

    var EventHandler = function(options) {
      if (options.templateUrl) {
        $http.get(options.templateUrl, {cache: true}).then(function(response){
          this.template = $compile(response.data);
        });
      } else {
        this.template = $compile(options.template);
      }

      if (options.render) {
        this.render = options.render;
      }
    };

    EventHandler.prototype.render = function(event) {
      return this.template({event: event});
    };

    return {
      registerType: function(type, options) {
        var eventHandler = new EventHandler(options);

        _registry[type] = eventHandler;

        return this;
      },
      renderEvent: function(event) {
        if (_registry[event.type] === undefined) {
          throw new Error('No event renderer found for type: ' + event.type);
        }
        return _registry[event.type].render(event);
      }
    };
  };

  angular.module('sentry.eventManager', [])
    .factory('EventManager', EventManager)
    .directive('renderEvent', function(EventManager){
      return {
        restrict: 'AE',
        link: function(scope, element, attrs, ctrl) {
          var evt = scope.$eval(attrs.renderEvent);
          element.html(EventManager.renderEvent(evt));
        }
      };
    });
});
