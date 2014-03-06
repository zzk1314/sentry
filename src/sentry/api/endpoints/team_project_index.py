from sentry.api.base import Endpoint
from sentry.api.permissions import assert_perm
from sentry.api.serializers import serialize
from sentry.models import Team, Project
from rest_framework.response import Response


class TeamProjectIndexEndpoint(Endpoint):
    def get(self, request, team_id):
        team = Team.objects.get_from_cache(id=team_id)

        assert_perm(team, request.user)

        results = list(Project.objects.get_for_user(request.user, team=team))

        return Response(serialize(results))
