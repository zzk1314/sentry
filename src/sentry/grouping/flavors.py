from __future__ import absolute_import

from sentry.constants import get_integration_id_for_event, VALID_PLATFORMS


def get_event_flavor_keys(data):
    """Returns all flavor keys for this event.  The event flavor keys are
    used to "freeze" the most likely used strategy for a project so that
    the user can explicitly upgrade later.

    The order in which the keys are returned go from lst specific to most
    specific.
    """
    rv = ['generic']

    platform = data.get('platform')
    if platform:
        if platform in VALID_PLATFORMS:
            rv.append('platform:%s' % platform)

    sdk_info = data.get('sdk_info')

    if platform and sdk_info and isinstance(sdk_info, dict):
        sdk_name = sdk_info.get('name')
        integrations = sdk_info.get('integrations')
        if sdk_name:
            for match in reversed(get_integration_id_for_event(
                    platform, sdk_name, integrations, return_matches=True)):
                rv.append('integration:%s' % match)

    return rv
