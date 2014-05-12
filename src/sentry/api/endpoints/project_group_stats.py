from rest_framework import status
from rest_framework.response import Response

from sentry.app import tsdb
from sentry.api.base import BaseStatsEndpoint
from sentry.api.permissions import assert_perm
from sentry.models import Project, Group


class ProjectGroupStatsEndpoint(BaseStatsEndpoint):
    def get(self, request, project_id):
        project = Project.objects.get(
            id=project_id,
        )

        assert_perm(project, request.user, request.auth)

        group_ids = map(int, request.QUERY_PARAMS.getlist('gID'))
        if not group_ids:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        group_ids = Group.objects.filter(
            id__in=group_ids, project=project,
        ).values_list('id', flat=True)

        data = tsdb.get_range(
            model=tsdb.models.group,
            keys=group_ids,
            **self._parse_args(request)
        )

        return Response(data)
