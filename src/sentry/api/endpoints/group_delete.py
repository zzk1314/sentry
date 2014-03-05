from sentry.api.base import Endpoint
from sentry.models import Group

from rest_framework.response import Response


class GroupDeleteEndpoint(Endpoint):
    def post(self, request, group_id):
        group = Group.objects.get(
            id=group_id,
        )
        group.delete()

        return Response()
