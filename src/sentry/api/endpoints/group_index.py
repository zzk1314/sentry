from rest_framework.response import Response

from sentry.api.base import Endpoint
from sentry.api.permissions import assert_perm
from sentry.api.serializers import serialize
from sentry.models import Project
from sentry.web.frontend.groups import _get_group_list


class GroupIndexEndpoint(Endpoint):
    def get(self, request, project_id):
        offset = 0
        limit = 100

        project = Project.objects.get(
            id=project_id,
        )

        assert_perm(project, request.user)

        response = _get_group_list(
            request=request,
            project=project,
        )

        group_list = response['event_list']
        group_list = list(group_list[offset:limit])

        results = serialize(group_list, request)

        return Response(results)
