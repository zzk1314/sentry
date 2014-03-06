from django.core.urlresolvers import reverse
from sentry.models import Team
from sentry.testutils import APITestCase


class TeamDetailsTest(APITestCase):
    def test_simple(self):
        team = self.team  # force creation
        self.client.force_authenticate(user=self.user)
        url = reverse('sentry-api-0-team-details', kwargs={'team_id': team.id})
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data['id'] == str(team.id)


class TeamUpdateTest(APITestCase):
    def test_simple(self):
        team = self.team  # force creation
        self.client.force_authenticate(user=self.user)
        url = reverse('sentry-api-0-team-details', kwargs={'team_id': team.id})
        response = self.client.put(url, data={
            'name': 'hello world',
            'slug': 'foobar',
        })
        assert response.status_code == 200
        team = Team.objects.get(id=team.id)
        assert team.name == 'hello world'
        assert team.slug == 'foobar'
