from __future__ import absolute_import

from django.core.urlresolvers import reverse
from exam import fixture

from sentry.testutils import APITestCase


class ProjectAlertsRulesConfigTest(APITestCase):
    @fixture
    def path(self):
        return reverse('sentry-api-0-project-alerts-rules-config', args=[
            self.organization.slug,
            self.project.slug,
        ])

    def test_simple(self):
        self.login_as(user=self.user)
        response = self.client.get(self.path)
        assert response.status_code == 200
        assert 'actions' in response.data
        assert 'conditions' in response.data
