define(['app', 'angular'], function(app, angular){
  'use strict';

  app.directive('prettyJson', function() {
    return {
      restrict: 'AC',
      link: function(scope, element, attrs) {
        element.text(angular.toJson(scope.$eval(attrs.prettyJson), true));
      }
    };
  });
});
