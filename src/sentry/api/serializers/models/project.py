from sentry.api.serializers import Serializer, register
from sentry.constants import MEMBER_OWNER
from sentry.models import Project, Team


@register(Project)
class ProjectSerializer(Serializer):
    def attach_metadata(self, objects, user):
        team_map = dict(
            (t.id, t) for t in Team.objects.get_for_user(user).itervalues()
        )
        for project in objects:
            try:
                project.access_type = team_map.get(project.team_id).access_type
            except KeyError:
                project.access_type = None

    def serialize(self, obj, user):
        d = {
            'id': str(obj.id),
            'slug': obj.slug,
            'name': obj.name,
            'dateCreated': obj.date_added,
            'permission': {
                'edit': obj.access_type == MEMBER_OWNER,
            }
        }
        return d
