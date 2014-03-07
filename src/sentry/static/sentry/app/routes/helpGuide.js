define(['app'], function() {
    'use strict';

    return {
        parent: 'help',
        url: 'guide/:language/',
        templateUrl: '/_static/sentry/app/templates/help-guide.html',
        controller: function(teamList, $scope, languageInfo){
            $scope.teamList = teamList.data;
            $scope.languageInfo = languageInfo;
        },
        resolve: {
            teamList: function($http, $stateParams) {
              return $http.get('/api/0/teams/');
            },
            languageInfo: function($http, $stateParams) {
                return {'install': 'pip install raven', 
                        'initialize': "from raven import Client\n\nclient = Client('{% if dsn %}{% else %}SENTRY_DSN{% endif %}')",
                        'simpleMessage': "Record a simple message\nclient.captureMessage('hello world!')\n\n# Capture an exception\ntry:\n\t1 / 0\nexcept ZeroDivisionError:\n\tclient.captureException()",
                        'middleware': 'from raven.middleware import Sentry\n\napplication = Sentry(application, client=client)',
                        'testConnection': 'raven test {% if dsn %}{{ dsn }}{% else %}SENTRY_DSN{% endif %}'
                    };
            }
        }
    };
});
