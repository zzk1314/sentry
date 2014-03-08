from rest_framework.response import Response

from sentry.api.base import Endpoint
from sentry.api.permissions import assert_perm
from sentry.models import Project


class ProjectStatsEndpoint(Endpoint):
    def get(self, request, project_id):
        project = Project.objects.get(
            id=project_id,
        )

        assert_perm(project, request.user)

        data = Project.objects.get_chart_data(
            instances=project,
            max_days=min(int(request.GET.get('days', 1)), 30),
        )

        return Response(data)
