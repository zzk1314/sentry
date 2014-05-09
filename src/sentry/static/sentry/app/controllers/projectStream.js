define(['app'], function(app) {
    'use strict';

    app.classy.controller({
        name: 'ProjectStreamCtrl',

        inject: ['$scope', '$window'],

        init: function() {
            this.$scope.groupList = this.$window.groupList;
        }
    });
});
