from __future__ import absolute_import

from sentry.grouping.flavors import get_event_flavor_keys


def test_flavor_keys_python_integration():
    data = {
        'platform': 'python',
        'sdk': {
            'name': 'raven-python',
            'integrations': ['tornado'],
        }
    }

    keys = get_event_flavor_keys(data)
    assert keys == [
        'generic',
        'platform:python',
        'integration:python',
        'integration:python-tornado',
    ]


def test_flavor_keys_sentry_cocoa():
    data = {
        'platform': 'cocoa',
        'sdk': {
            'name': 'sentry-cocoa'
        }
    }

    keys = get_event_flavor_keys(data)
    assert keys == [
        'generic',
        'platform:cocoa',
        'integration:cocoa'
    ]
