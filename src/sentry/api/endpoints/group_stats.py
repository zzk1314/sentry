from sentry.api.base import Endpoint
from sentry.models import Group

from rest_framework.response import Response


class GroupStatsEndpoint(Endpoint):
    def get(self, request, group_id):
        group = Group.objects.get(
            id=group_id,
        )

        data = Group.objects.get_chart_data_for_group(
            instances=[group],
            max_days=3,
        )

        return Response(data)
