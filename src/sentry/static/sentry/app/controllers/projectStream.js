/*jshint -W024 */

define([
  'app',

  'app/utils'
], function(app, utils) {
  'use strict';

  app.classy.controller({
    name: 'ProjectStreamCtrl',

    inject: ['config', '$http', '$scope', '$window', '$timeout'],

    init: function() {
      this.$scope.groupList = this.$window.groupList;

      this.$timeout(this.pollForChanges, 1000);
    },

    pollForChanges: function() {
      var self = this;

      this.$http.get('/api/0/projects/' + this.config.projectId + '/groups/').success(function(data){
        angular.extend(self.$scope.groupList, data);

        utils.sortArray(self.$scope.groupList, function(item){
          return [new Date(item.lastSeen).getTime()];
        }).slice(0, 50);

      }).finally(function(){
        self.$timeout(self.pollForChanges, 1000);
      });
    }
  });
});
