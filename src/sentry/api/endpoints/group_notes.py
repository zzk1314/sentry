from sentry.api.base import Endpoint
from sentry.api.serializers import serialize
from sentry.models import Group

from rest_framework.response import Response


class GroupNotesEndpoint(Endpoint):
    def get(self, request, group_id):
        group = Group.objects.get(
            id=group_id,
        )
        return Response(serialize(group))
