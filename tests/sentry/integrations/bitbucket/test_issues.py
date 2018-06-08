from __future__ import absolute_import

import responses

from exam import fixture

from django.test import RequestFactory

from sentry.models import Integration
from sentry.testutils import TestCase

from sentry.integrations.bitbucket.integration import BitbucketIntegration


class BitbucketPluginTest(TestCase):
    @fixture
    def integration(self):
        return BitbucketIntegration()

    @fixture
    def request(self):
        return RequestFactory()

    def setUp(self):
        self.user = self.create_user()
        self.organization = self.create_organization()

        model = Integration.objects.create(
            provider='bitbucket',
            external_id='bitbucket_external_id',
            name='maxbittker/newsdiffs',
            metadata={
                'base_url': 'https://api.bitbucket.org',
                'shared_secret': '1234567890',
            }
        )
        model.add_organization(self.add_organization(self.organization.id))
        self.integration = BitbucketIntegration(model)

    def test_get_issue_label(self):
        group = self.create_group(message='Hello world', culprit='foo.bar')
        assert self.integration.get_issue_label(group, 1) == 'Bitbucket-1'

    def test_get_issue_url(self):
        group = self.create_group(message='Hello world', culprit='foo.bar')
        assert self.integration.get_issue_url(
            group, 1
        ) == 'https://bitbucket.org/maxbittker/newsdiffs/issue/1/'

    @responses.activate
    def test_create_issue(self):
        responses.add(
            responses.POST,
            'https://api.bitbucket.org/1.0/repositories/maxbittker/newsdiffs/issues',
            json={"local_id": 1, "title": "Hello world"}
        )
        group = self.create_group(message='Hello world', culprit='foo.bar')

        request = self.request.get('/')
        form_data = {
            'title': 'Hello',
            'description': 'Fix this.',
            'issue_type': 'bug',
            'priority': 'trivial'
        }

        assert self.integration.create_issue(request, group, form_data) == 1
        request = responses.calls[-1].request
        assert request.headers.get('Authorization', '').startswith('OAuth ')

    @responses.activate
    def test_link_issue(self):
        responses.add(
            responses.GET,
            'https://api.bitbucket.org/1.0/repositories/maxbittker/newsdiffs/issues/1',
            json={"local_id": 1, "title": "Hello world"}
        )
        responses.add(
            responses.POST,
            'https://api.bitbucket.org/1.0/repositories/maxbittker/newsdiffs/issues/1/comments',
            json={"body": "Hello"}
        )

        self.integration.set_option('repo', 'maxbittker/newsdiffs', self.project)
        group = self.create_group(message='Hello world', culprit='foo.bar')

        request = self.request.get('/')
        form_data = {
            'comment': 'Hello',
            'issue_id': '1',
        }

        assert self.integration.link_issue(request, group, form_data) == {
            'title': 'Hello world',
        }
