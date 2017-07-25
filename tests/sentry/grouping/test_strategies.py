from __future__ import absolute_import

from exam import fixture

from sentry.testutils import TestCase
from sentry.interfaces.exception import Exception
from sentry.grouping.flavors import get_event_flavor_keys
from sentry.grouping.strategies.api import pick_strategies


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


class ExceptionBasicsTest(TestCase):

    @fixture
    def interface(self):
        return Exception.to_python(dict(values=[{
            'type': 'ValueError',
            'value': 'hello world',
            'module': 'foo.bar',
            'stacktrace': {'frames': [{
                'filename': 'foo/baz.py',
                'lineno': 1,
                'in_app': True,
            }]},
        }, {
            'type': 'ValueError',
            'value': 'hello world',
            'module': 'foo.bar',
            'stacktrace': {'frames': [{
                'filename': 'foo/baz.py',
                'lineno': 1,
                'in_app': True,
            }]},
        }]))

    def test_basics(self):
        org = self.create_organization()
        project = self.create_project(organization=org)
        pick = pick_strategies(project, data={
            'platform': 'python',
            'sentry.interfaces.Exception': self.interface.to_json(),
        })

        assert pick is not None

        assert pick.flavor_keys == ['generic', 'platform:python']
        assert pick.platform == 'python'
        assert pick.project is project
        assert pick.new_strategies == [
            ('generic-exception', '1.0', 'generic'),
            ('generic-in-app-exception', '1.0', 'generic'),
        ]
