from django.utils import timezone

from sentry.api.base import Endpoint
from sentry.db.models import create_or_update
from sentry.models import Group, GroupSeen

from rest_framework.response import Response


class GroupMarkSeenEndpoint(Endpoint):
    def post(self, request, group_id):
        group = Group.objects.get(
            id=group_id,
        )

        create_or_update(
            GroupSeen,
            group=group,
            user=request.user,
            project=group.project,
            defaults={
                'last_seen': timezone.now(),
            }
        )

        return Response()
