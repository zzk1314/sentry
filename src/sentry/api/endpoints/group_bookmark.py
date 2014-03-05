from sentry.api.base import Endpoint
from sentry.models import Group, GroupBookmark

from rest_framework.response import Response


class GroupBookmarkEndpoint(Endpoint):
    def post(self, request, group_id):
        group = Group.objects.get(
            id=group_id,
        )

        bookmark = GroupBookmark(
            project=group.project,
            group=group,
            user=request.user,
        )

        bookmark.save()

        return Response()
