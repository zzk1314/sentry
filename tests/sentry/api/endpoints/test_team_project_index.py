from django.core.urlresolvers import reverse
from sentry.testutils import APITestCase


class TeamProjectIndexTest(APITestCase):
    def test_simple(self):
        self.client.force_authenticate(user=self.user)
        team = self.create_team(slug='baz')
        project_1 = self.create_project(team=team, slug='fiz')
        project_2 = self.create_project(team=team, slug='buzz')

        url = reverse('sentry-api-0-team-project-index', kwargs={
            'team_id': team.id,
        })
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 2
        assert sorted(map(lambda x: x['id'], response.data)) == sorted([
            str(project_1.id),
            str(project_2.id),
        ])
