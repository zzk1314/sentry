from django.core.urlresolvers import reverse
from sentry.testutils import APITestCase


class GroupNoteTest(APITestCase):
    def test_simple(self):
        self.client.force_authenticate(user=self.user)

        url = reverse('sentry-api-0-group-notes', kwargs={
            'group_id': self.group.id,
        })
        response = self.client.get(url, format='json')
        assert response.status_code == 200, response.content
