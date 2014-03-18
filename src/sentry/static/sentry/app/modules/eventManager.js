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

  var EventManager = function(){
    var _registry = {};

    return {
      registerType: function(type, object) {
        _registry[type] = object;

        return this;
      },
      renderEvent: function(event) {
        if (_registry[event.type] === undefined) {
          throw new Error('No event renderer found for type: ' + event.type);
        }
        return _registry[event.type](event).render();
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
