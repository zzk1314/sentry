from sentry.api.base import Endpoint
from sentry.api.serializers import serialize
from sentry.models import Team
from rest_framework.response import Response


class TeamMemberIndexEndpoint(Endpoint):
    def get(self, request, team_id):
        team = Team.objects.get_from_cache(id=team_id)

        member_list = serialize(list(team.member_set.select_related('user')))
        member_list.extend(serialize(list(team.pending_member_set.all())))
        member_list.sort(key=lambda x: x['email'])

        return Response(member_list)
