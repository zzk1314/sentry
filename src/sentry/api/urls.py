from django.conf.urls import patterns, url

from .endpoints.event_details import EventDetailsEndpoint
from .endpoints.group_index import GroupIndexEndpoint
from .endpoints.group_details import GroupDetailsEndpoint
from .endpoints.group_resolve import GroupResolveEndpoint
from .endpoints.group_bookmark import GroupBookmarkEndpoint
from .endpoints.group_markseen import GroupMarkSeenEndpoint
from .endpoints.group_delete import GroupDeleteEndpoint
from .endpoints.group_events import GroupEventsEndpoint
from .endpoints.group_events_latest import GroupEventsLatestEndpoint
from .endpoints.group_notes import GroupNotesEndpoint
from .endpoints.group_stats import GroupStatsEndpoint
from .endpoints.project_index import ProjectIndexEndpoint
from .endpoints.team_index import TeamIndexEndpoint
from .endpoints.team_project_index import TeamProjectIndexEndpoint
from .endpoints.team_member_index import TeamMemberIndexEndpoint


urlpatterns = patterns(
    '',

    # Teams
    url(r'^teams/$',
        TeamIndexEndpoint.as_view(),
        name='sentry-api-0-team-index'),
    url(r'^teams/(?P<team_id>\d+)/projects/$',
        TeamProjectIndexEndpoint.as_view(),
        name='sentry-api-0-team-project-index'),
    url(r'^teams/(?P<team_id>\d+)/members/$',
        TeamMemberIndexEndpoint.as_view(),
        name='sentry-api-0-team-member-index'),

    # Projects
    url(r'^projects/$',
        ProjectIndexEndpoint.as_view(),
        name='sentry-api-0-project-index'),
    url(r'^projects/(?P<project_id>\d+)/groups/$',
        GroupIndexEndpoint.as_view(),
        name='sentry-api-0-group-list'),

    # Groups
    url(r'^groups/(?P<group_id>\d+)/$',
        GroupDetailsEndpoint.as_view(),
        name='sentry-api-0-group-details'),
    url(r'^groups/(?P<group_id>\d+)/resolve/$',
        GroupResolveEndpoint.as_view(),
        name='sentry-api-0-group-resolve'),
    url(r'^groups/(?P<group_id>\d+)/bookmark/$',
        GroupBookmarkEndpoint.as_view(),
        name='sentry-api-0-group-bookmark'),
    url(r'^groups/(?P<group_id>\d+)/markseen/$',
        GroupMarkSeenEndpoint.as_view(),
        name='sentry-api-0-group-markseen'),
    url(r'^groups/(?P<group_id>\d+)/delete/$',
        GroupDeleteEndpoint.as_view(),
        name='sentry-api-0-group-delete'),
    url(r'^groups/(?P<group_id>\d+)/events/$',
        GroupEventsEndpoint.as_view(),
        name='sentry-api-0-group-events'),
    url(r'^groups/(?P<group_id>\d+)/events/latest/$',
        GroupEventsLatestEndpoint.as_view(),
        name='sentry-api-0-group-events-latest'),
    url(r'^groups/(?P<group_id>\d+)/notes/$',
        GroupNotesEndpoint.as_view(),
        name='sentry-api-0-group-notes'),
    url(r'^groups/(?P<group_id>\d+)/stats/$',
        GroupStatsEndpoint.as_view(),
        name='sentry-api-0-group-stats'),

    # Events
    url(r'^events/(?P<event_id>\d+)/$',
        EventDetailsEndpoint.as_view(),
        name='sentry-api-0-event-details'),

    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
