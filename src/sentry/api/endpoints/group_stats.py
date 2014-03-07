from rest_framework.response import Response

from sentry.api.base import Endpoint
from sentry.api.permissions import assert_perm
from sentry.models import Group


class GroupStatsEndpoint(Endpoint):
    def get(self, request, group_id):
        group = Group.objects.get(
            id=group_id,
        )

        assert_perm(group, request.user)

        data = Group.objects.get_chart_data_for_group(
            instances=[group],
            max_days=min(int(request.GET.get('days', 1)), 30),
        )

        return Response(data)
