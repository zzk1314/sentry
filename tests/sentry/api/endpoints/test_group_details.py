from django.core.urlresolvers import reverse
from sentry.testutils import APITestCase


class GroupDetailsTest(APITestCase):
    def test_simple(self):
        self.client.force_authenticate(user=self.user)

        group = self.create_group()

        url = reverse('sentry-api-0-group-details', kwargs={
            'group_id': group.id,
        })
        response = self.client.get(url, format='json')

        assert response.status_code == 200, response.content
        assert response.data['id'] == str(group.id)
