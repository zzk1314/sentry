define(['app', 'moment', 'jquery'], function(app, moment, $) {
    'use strict';

    app.directive('timeSince', function($timeout) {
        return function timeSince(scope, element, attrs) {
            var $element = $(element),
                timeout_id;

            function update(value){
                if (!value || value === undefined) {
                    return '';
                }

                $element.text(moment.utc(value).fromNow());
            }

            function tick(){
                update(scope.$eval(attrs.timeSince));
                timeout_id = $timeout(tick, 1000);
            }

            scope.$watch(attrs.timeSince, update);

            element.bind('$destroy', function() {
                if (timeout_id) {
                    $timeout.cancel(timeout_id);
                }
            });

            tick();
        };
    });
});
