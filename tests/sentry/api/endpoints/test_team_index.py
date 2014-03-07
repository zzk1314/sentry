from django.core.urlresolvers import reverse
from sentry.models import Team
from sentry.testutils import APITestCase


class TeamIndexTest(APITestCase):
    def test_simple(self):
        team = self.team  # force creation
        self.client.force_authenticate(user=self.user)
        url = reverse('sentry-api-0-team-index')
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['id'] == str(team.id)


class TeamCreateTest(APITestCase):
    def test_simple(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('sentry-api-0-team-index')
        resp = self.client.post(url, data={
            'name': 'hello world',
            'slug': 'foobar',
        })
        assert resp.status_code == 201, resp.content
        team = Team.objects.get(id=resp.data['id'])
        assert team.name == 'hello world'
        assert team.slug == 'foobar'
        assert team.owner == self.user
