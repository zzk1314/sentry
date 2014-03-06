from sentry.api.base import Endpoint
from sentry.api.permissions import assert_perm
from sentry.api.serializers import serialize
from sentry.models import Project
from sentry.web.frontend.groups import _get_group_list


class ProjectGroupIndexEndpoint(Endpoint):
    def get(self, request, project_id):
        project = Project.objects.get(
            id=project_id,
        )

        assert_perm(project, request.user)

        response = _get_group_list(
            request=request,
            project=project,
        )

        queryset = response['event_list']

        return self.paginate(
            request=request,
            queryset=queryset,
            order_by='-last_seen',
            on_results=lambda x: serialize(x, request.user),
        )
