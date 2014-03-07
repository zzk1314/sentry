define(['app'], function() {
    'use strict';

    return {
        parent: 'help',
        url: 'guide/:language/',
        templateUrl: 'partials/help-guide.html',
        controller: function($scope){
            $scope.languageInfo = {
                'install': 'pip install raven',
                'initialize': "from raven import Client\n\nclient = Client('{% if dsn %}{% else %}SENTRY_DSN{% endif %}')",
                'simpleMessage': "Record a simple message\nclient.captureMessage('hello world!')\n\n# Capture an exception\ntry:\n\t1 / 0\nexcept ZeroDivisionError:\n\tclient.captureException()",
                'middleware': 'from raven.middleware import Sentry\n\napplication = Sentry(application, client=client)',
                'testConnection': 'raven test {% if dsn %}{{ dsn }}{% else %}SENTRY_DSN{% endif %}'
            };
        }
    };
});
