define([
  'angular',
  'ngBootstrap',
  'ngHttpAuth'
], function(angular) {
  'use strict';

  angular.module('sentry.auth', ['http-auth-interceptor', 'sentry.forms', 'ui.bootstrap'])
    .directive('authFrame', function($modal) {
      return {
        restrict: 'A',
        link: function(scope, element, attrs, ctrl) {
          scope.$on('event:auth-loginRequired', function(event, response) {
            var needsSudo = (response.data.sudoRequired === true);
            var templateUrl = needsSudo ? 'login-sudo.html' : 'login.html';

            var modal = $modal.open({
              templateUrl: 'partials/' + templateUrl,
              controller: function($scope, $http, $state, authService, Form){
                $scope.authForm = new Form({
                  username: {
                    type: 'text',
                    placeholder: 'walter.white@example.com',
                    required: true
                  },
                  password: {
                    type: 'password',
                    placeholder: 'password',
                    required: true
                  }
                }, {
                  username: response.data.username || null
                });

                function addAuthHeader(data, headersGetter){
                  // as per HTTP authentication spec [1], credentials must be
                  // encoded in base64. Lets use window.btoa [2]
                  var headers = headersGetter();
                  headers.Authorization = 'Basic ' + btoa(data.username + ':' + data.password);
                }

                $scope.saveForm = function() {
                  var data = $scope.authForm.getData();
                  if (needsSudo) {
                    data.username = response.data.username;
                  }

                  $http({
                    method: 'POST',
                    url: '/api/0/auth/',
                    data: data,
                    transformRequest: addAuthHeader
                  }).success(function(data){
                    authService.loginConfirmed(data);
                    modal.close();
                  });
                };
              }
            });
          });
        }
      };
    });
});
