define([
    'backbone',

    'text!app/templates/group.html'
], function(Backbone, groupTemplate){
    'use strict';

    return {
        group: groupTemplate
    };
});
