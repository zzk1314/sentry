from rest_framework.response import Response

from sentry.api.base import Endpoint
from sentry.api.serializers import serialize
from sentry.models import Team


class UserDetailsEndpoint(Endpoint):
    def get(self, request, user_id):
        if user_id == 'me':
            user = request.user
        else:
            return Response(status=403)

        teams = Team.objects.get_for_user(user, with_projects=True)

        data = serialize(user, request.user)
        data['teams'] = serialize([t[0] for t in teams.itervalues()], request.user)
        for (team, projects), team_data in zip(teams.itervalues(), data['teams']):
            team_data['projects'] = serialize(projects, request.user)

        return Response(data)
