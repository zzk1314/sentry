from __future__ import absolute_import

from exam import fixture

from sentry.testutils import TestCase
from sentry.interfaces.exception import Exception
from sentry.grouping.flavors import get_event_flavor_keys
from sentry.grouping.strategies.api import pick_strategies, \
    describe_strategy_grouping


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
            'value': 'invalid value',
            'module': 'foo.bar',
            'stacktrace': {'frames': [{
                'filename': 'foo/bar.py',
                'function': 'convert_value',
                'lineno': 42,
                'in_app': True,
            }]},
        }, {
            'type': 'LookupError',
            'value': 'mykey',
            'module': 'foo.bar',
            'stacktrace': {'frames': [{
                'filename': 'foo/bar.py',
                'function': 'main',
                'lineno': 97,
                'in_app': True,
            }, {
                'filename': 'foo/bar.py',
                'function': 'lookup_item',
                'lineno': 23,
                'in_app': True,
            }]},
        }]))

    def test_basics(self):
        org = self.create_organization()
        project = self.create_project(organization=org)
        data = {
            'platform': 'python',
            'sentry.interfaces.Exception': self.interface.to_json(),
        }
        pick = pick_strategies(project, data=data)

        assert pick is not None

        assert pick.flavor_keys == ['generic', 'platform:python']
        assert pick.platform == 'python'
        assert pick.project is project
        assert pick.new_strategies == [
            ('generic-in-app-exception', '1.0', 'generic'),
            ('generic-exception', '1.0', 'generic'),
        ]

        values = pick.process_data(data, all=True)

        readable = describe_strategy_grouping(values[0], as_text=True)
        assert readable.splitlines() == [
            'group by exception',
            '  considering in-app stacktrace',
            '  considering in-app stacktrace',
        ]

        readable = describe_strategy_grouping(values[1], as_text=True)
        assert readable.splitlines() == [
            'group by exception',
            '  considering complete stacktrace',
            '  considering complete stacktrace',
        ]
