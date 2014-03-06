from django import forms
from rest_framework import status
from rest_framework.response import Response

from sentry.api.base import Endpoint
from sentry.constants import MEMBER_ADMIN
from sentry.api.permissions import assert_perm
from sentry.api.serializers import serialize
from sentry.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'slug')


class TeamDetailsEndpoint(Endpoint):
    def get(self, request, team_id):
        team = Team.objects.get(id=team_id)

        assert_perm(team, request.user)

        return Response(serialize(team, request.user))

    def put(self, request, team_id):
        team = Team.objects.get(id=team_id)

        assert_perm(team, request.user, type=MEMBER_ADMIN)

        form = TeamForm(request.DATA, instance=team)
        if not form.is_valid():
            return Response('{"error": "form"}', status=status.HTTP_400_BAD_REQUEST)

        team = form.save()

        return Response(serialize(team, request.user))
