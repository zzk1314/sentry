from rest_framework import serializers, status
from sentry.api.base import Endpoint
from sentry.api.permissions import assert_perm
from sentry.api.serializers import serialize
from sentry.constants import MEMBER_ADMIN
from sentry.models import Team, AccessGroup
from rest_framework.response import Response


class AccessGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessGroup
        fields = ('name', 'type')


class TeamAccessGroupIndexEndpoint(Endpoint):
    def get(self, request, team_id):
        team = Team.objects.get_from_cache(id=team_id)

        assert_perm(team, request.user)

        data = sorted(AccessGroup.objects.filter(team=team), key=lambda x: x.name)

        return Response(serialize(data, request.user))

    def post(self, request, team_id):
        team = Team.objects.get_from_cache(id=team_id)

        assert_perm(team, request.user, MEMBER_ADMIN)

        serializer = AccessGroupSerializer(data=request.DATA)

        if serializer.is_valid():
            access_group = serializer.object
            access_group.team = team
            access_group.managed = False
            access_group.save()
            return Response(serialize(access_group, request.user), status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
