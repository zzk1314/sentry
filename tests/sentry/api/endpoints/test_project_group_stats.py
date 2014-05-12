from django.core.urlresolvers import reverse

from sentry.app import tsdb
from sentry.testutils import APITestCase


class ProjectGroupStatsTest(APITestCase):
    def test_simple(self):
        self.login_as(user=self.user)

        project = self.create_project()
        group1 = self.create_group(project=project)
        group2 = self.create_group(project=project)

        tsdb.incr(tsdb.models.group, group1.id, count=3)
        tsdb.incr(tsdb.models.group, group2.id, count=5)

        url = reverse('sentry-api-0-project-group-stats', kwargs={
            'project_id': project.id,
        })
        response = self.client.get(url, {'gID': [group1.id, group2.id]}, format='json')

        assert response.status_code == 200, response.content
        assert len(response.data) == 2
        assert group1.id in response.data
        assert group2.id in response.data
