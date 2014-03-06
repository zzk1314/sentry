from django.utils import timezone
from rest_framework.response import Response

from sentry.api.base import Endpoint
from sentry.api.permissions import assert_perm
from sentry.db.models import create_or_update
from sentry.models import Group, GroupSeen


class GroupMarkSeenEndpoint(Endpoint):
    def post(self, request, group_id):
        group = Group.objects.get(
            id=group_id,
        )

        assert_perm(group, request.user)

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
