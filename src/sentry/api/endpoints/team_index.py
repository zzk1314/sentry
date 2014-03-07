from rest_framework import serializers, status
from rest_framework.response import Response

from sentry.api.base import Endpoint
from sentry.api.serializers import serialize
from sentry.models import Team
from sentry.permissions import can_create_teams


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'slug')


class TeamIndexEndpoint(Endpoint):
    def get(self, request):
        teams = Team.objects.get_for_user(request.user).values()
        return Response(serialize(teams, request.user))

    def post(self, request):
        if not can_create_teams(request.user):
            return Response(status=403)

        serializer = TeamSerializer(data=request.DATA)

        if serializer.is_valid():
            team = serializer.object
            team.owner = request.user
            team.save()
            return Response(serialize(team, request.user), status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
