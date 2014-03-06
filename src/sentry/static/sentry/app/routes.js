define([
    'app',
    'routes/eventDetails',
    'routes/groupDetails',
    'routes/index',
    'routes/manageTeam',
    'routes/manageTeamAccessGroups',
    'routes/manageTeamMembers',
    'routes/manageTeamProjects',
    'routes/manageTeamSettings',
    'routes/projectDetails',
    'routes/projectStream',
    'routes/teamDetails',

    // registration via loader
    'filters/formatNumber'
], function(
    app,
    EventDetailsRoute,
    GroupDetailsRoute,
    IndexRoute,
    ManageTeamRoute,
    ManageTeamAccessGroupsRoute,
    ManageTeamMembersRoute,
    ManageTeamProjectsRoute,
    ManageTeamSettingsRoute,
    ProjectDetailsRoute,
    ProjectStreamRoute,
    TeamDetailsRoute
) {
    'use strict';

    app.config(function($locationProvider, $stateProvider, $httpProvider, $urlRouterProvider,
                        $uiViewScrollProvider) {
        // use html5 location rather than hashes
        $locationProvider.html5Mode(true);

        $urlRouterProvider.otherwise("/");

        // revert to default scrolling behavior as autoscroll is broken
        $uiViewScrollProvider.useAnchorScroll();

        // on a 401 (from the API) redirect the user to the login view
        var logInUserOn401 = ['$window', '$q', function($window, $q) {
            function success(response) {
                return response;
            }

            function error(response) {
                if(response.status === 401) {
                    $window.location.href = '/login/';
                    return $q.reject(response);
                }
                else {
                    return $q.reject(response);
                }
            }

            return function(promise) {
                return promise.then(success, error);
            };
        }];
        $httpProvider.responseInterceptors.push(logInUserOn401);

        // and now our routes
        $stateProvider
            .state('event', EventDetailsRoute)
            .state('group', GroupDetailsRoute)
            .state('index', IndexRoute)
            .state('project', ProjectDetailsRoute)
            .state('project.stream', ProjectStreamRoute)
            .state('team', TeamDetailsRoute)
            .state('manage_team', ManageTeamRoute)
            .state('manage_team.access_groups', ManageTeamAccessGroupsRoute)
            .state('manage_team.members', ManageTeamMembersRoute)
            .state('manage_team.projects', ManageTeamProjectsRoute)
            .state('manage_team.settings', ManageTeamSettingsRoute);
    });
});
