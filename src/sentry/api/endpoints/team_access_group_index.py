from sentry.api.base import Endpoint
from sentry.api.permissions import assert_perm
from sentry.api.serializers import serialize
from sentry.models import Team, AccessGroup
from rest_framework.response import Response


class TeamAccessGroupIndexEndpoint(Endpoint):
    def get(self, request, team_id):
        team = Team.objects.get_from_cache(id=team_id)

        assert_perm(team, request.user)

        data = sorted(AccessGroup.objects.filter(team=team), key=lambda x: x.name)

        return Response(serialize(data, request.user))
