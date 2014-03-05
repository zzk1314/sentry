from django.utils.decorators import method_decorator

from sentry.api.base import Endpoint
from sentry.api.serializers import serialize
from sentry.models import Group
from sentry.web.decorators import has_access

from rest_framework.response import Response


class GroupDetailsEndpoint(Endpoint):
    @method_decorator(has_access)
    def get(self, request, group_id):
        group = Group.objects.get(
            id=group_id,
        )
        data = serialize(group)

        return Response(data)
