(function(app){
    "use strict";

    app.templates = {
        group: '' + 
            '<div class="count" data-count="<%= app.utils.formatNumber(count) %>"><span><%= app.utils.formatNumber(count) %></span></div>' + 
            '<div class="details">' + 
                '<h3><a href="<%= permalink %>"><%= title %></a></h3>' + 
                '<p class="message">' + 
                    '<span class="tag tag-logger"><%= logger %></span>' + 
                    '<% _.each(versions, function(version){ %> ' + 
                        '<span class="tag tag-version"><%= version %></span>' + 
                    '<% }) %>' + 
                    '<% _.each(tags, function(tag){ %> ' + 
                        '<span class="tag"><%= tag %></span>' + 
                    '<% }) %>' + 
                    '<%= message %>' + 
                '</p>' + 
                '<div class="meta">' + 
                    '<span class="last-seen pretty-date" title="<%= lastSeen %>"><%= app.utils.prettyDate(lastSeen) %></span>' + 
                    '<% if (timeSpent) { %>' + 
                        '<span class="time-spent"><%= Math.round(timeSpent) %>ms</span>' + 
                    '<% } %>' + 
                    '<span class="tag tag-project"><%= project.name %></span>' + 
                '</div>' + 
                '<span class="sparkline"></span>' + 
                '<ul class="actions">' + 
                    '<% if (canResolve) { %>' + 
                        '<li>' +
                            '<% if (isMuted) { %>' +
                                '<a href="#" class="checked" data-action="unmute" title="Unmute Updates"><i class="icon-bullhorn"></i></a>' + 
                            '<% } else if (isResolved) { %>' + 
                                '<a href="#" data-action="mute" title="Mute Future Updates"><i class="icon-volume-off"></i></a>' + 
                            '<% } else { %>' + 
                                '<a href="#" data-action="resolve" title="Mark as Resolved"><i class="icon-ok"></i></a>' + 
                            '<% } %>' + 
                        '</li>' + 
                        '<li>' + 
                            '<a href="#" data-action="bookmark" class="bookmark<% if (isBookmarked) { %> checked<% } %>" title="Bookmark"><i class="icon-star"></i></a>' + 
                        '</li>' + 
                    '<% } %>' + 
                '</ul>' + 
            '</div>' + 
        '</script>'
    };
}(app));