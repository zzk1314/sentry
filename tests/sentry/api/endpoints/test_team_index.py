from django.core.urlresolvers import reverse
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
