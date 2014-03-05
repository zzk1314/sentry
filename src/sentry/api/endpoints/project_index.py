from sentry.api.base import Endpoint
from sentry.api.serializers import serialize
from sentry.models import Project
from rest_framework.response import Response


class ProjectIndexEndpoint(Endpoint):
    def get(self, request):
        projects = list(Project.objects.get_for_user(request.user))
        return Response(serialize(projects))
