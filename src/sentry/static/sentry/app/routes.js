define([
    'app',
    'routes/createAccessGroup',
    'routes/createProject',
    'routes/createTeam',
    'routes/deleteProject',
    'routes/deleteTeam',
    'routes/eventDetails',
    'routes/groupDetails',
    'routes/groupNotes',
    'routes/groupTags',
    'routes/help',
    'routes/helpGuide',
    'routes/index',
    'routes/login',
    'routes/manageAccount',
    'routes/manageAccountSettings',
    'routes/manageAccountTeams',
    'routes/manageProject',
    'routes/manageProjectAPIKeys',
    'routes/manageProjectNotifications',
    'routes/manageProjectRateLimits',
    'routes/manageProjectSettings',
    'routes/manageProjectTags',
    'routes/manageTeam',
    'routes/manageTeamAccessGroups',
    'routes/manageTeamMembers',
    'routes/manageTeamOwnership',
    'routes/manageTeamProjects',
    'routes/manageTeamSettings',
    'routes/projectDetails',
    'routes/projectStream',
    'routes/teamDetails',

    // registration via loader
    'directives/autoFocus',
    'directives/prettyJson',
    'directives/timeSince',
    'filters/formatNumber'
], function(
    app,
    CreateAccessGroupRoute,
    CreateProjectRoute,
    CreateTeamRoute,
    DeleteProjectRoute,
    DeleteTeamRoute,
    EventDetailsRoute,
    GroupDetailsRoute,
    GroupNotesRoute,
    GroupTagsRoute,
    HelpRoute,
    HelpGuideRoute,
    IndexRoute,
    LoginRoute,
    ManageAccountRoute,
    ManageAccountSettingsRoute,
    ManageAccountTeamsRoute,
    ManageProjectRoute,
    ManageProjectAPIKeysRoute,
    ManageProjectNotificationsRoute,
    ManageProjectRateLimitsRoute,
    ManageProjectSettingsRoute,
    ManageProjectTagsRoute,
    ManageTeamRoute,
    ManageTeamAccessGroupsRoute,
    ManageTeamMembersRoute,
    ManageTeamOwnershipRoute,
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
        // $locationProvider.html5Mode(true);

        $urlRouterProvider.otherwise("/");

        // revert to default scrolling behavior as autoscroll is broken
        $uiViewScrollProvider.useAnchorScroll();

        // add in Django csrf support
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        // and now our routes
        $stateProvider
            .state('create_access_group', CreateAccessGroupRoute)
            .state('create_project', CreateProjectRoute)
            .state('create_team', CreateTeamRoute)
            .state('event', EventDetailsRoute)
            .state('group', GroupDetailsRoute)
            .state('group.notes', GroupNotesRoute)
            .state('group.tags', GroupTagsRoute)
            .state('help', HelpRoute)
            .state('help.guide', HelpGuideRoute)
            .state('index', IndexRoute)
            .state('login', LoginRoute)
            .state('project', ProjectDetailsRoute)
            .state('project.stream', ProjectStreamRoute)
            .state('team', TeamDetailsRoute)
            .state('manage_account', ManageAccountRoute)
            .state('manage_account.settings', ManageAccountSettingsRoute)
            .state('manage_account.teams', ManageAccountTeamsRoute)
            .state('manage_project', ManageProjectRoute)
            .state('manage_project.api_keys', ManageProjectAPIKeysRoute)
            .state('manage_project.delete', DeleteProjectRoute)
            .state('manage_project.notifications', ManageProjectNotificationsRoute)
            .state('manage_project.rate_limits', ManageProjectRateLimitsRoute)
            .state('manage_project.tags', ManageProjectTagsRoute)
            .state('manage_project.settings', ManageProjectSettingsRoute)
            .state('manage_team', ManageTeamRoute)
            .state('manage_team.access_groups', ManageTeamAccessGroupsRoute)
            .state('manage_team.delete', DeleteTeamRoute)
            .state('manage_team.members', ManageTeamMembersRoute)
            .state('manage_team.ownership', ManageTeamOwnershipRoute)
            .state('manage_team.projects', ManageTeamProjectsRoute)
            .state('manage_team.settings', ManageTeamSettingsRoute);
    });
});
