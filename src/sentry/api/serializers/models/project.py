from sentry.api.serializers import Serializer, register
from sentry.models import Project


@register(Project)
class ProjectSerializer(Serializer):
    def serialize(self, obj, user):
        d = {
            'id': str(obj.id),
            'slug': obj.slug,
            'name': obj.name,
            'dateCreated': obj.date_added,
        }
        return d
