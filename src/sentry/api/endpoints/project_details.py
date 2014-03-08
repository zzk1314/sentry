from rest_framework import serializers, status
from rest_framework.response import Response

from sentry.api.base import Endpoint
from sentry.constants import MEMBER_ADMIN
from sentry.api.permissions import assert_perm
from sentry.api.serializers import serialize
from sentry.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = Project
        fields = ('name', 'slug')


class ProjectDetailsEndpoint(Endpoint):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)

        assert_perm(project, request.user)

        data = serialize(project, request.user)
        data['options'] = {
            'sentry:origins': project.get_option('sentry:origins', None) or [],
            'sentry:resolve_age': int(project.get_option('sentry:resolve_age', 0)),
        }

        return Response(data)

    def put(self, request, project_id):
        project = Project.objects.get(id=project_id)

        assert_perm(project, request.user, access=MEMBER_ADMIN)

        serializer = ProjectSerializer(project, data=request.DATA, partial=True)

        if serializer.is_valid():
            project = serializer.save()
            return Response(serialize(project, request.user))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        project = Project.objects.get(id=project_id)

        if not (request.user.is_superuser or project.team.owner_id == request.user.id):
            return Response('{"error": "form"}', status=status.HTTP_403_FORBIDDEN)

        # TODO(dcramer): this needs to push it into the queue
        project.delete()

        return Response(status=204)
