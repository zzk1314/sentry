from sentry.api.base import Endpoint
from sentry.api.serializers import serialize
from sentry.models import Team

from rest_framework.response import Response


class TeamIndexEndpoint(Endpoint):
    def get(self, request):
        teams = Team.objects.get_for_user(request.user).values()
        return Response(serialize(teams))
