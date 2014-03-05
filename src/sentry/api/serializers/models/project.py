from sentry.api.serializers import Serializer, register
from sentry.models import Project


@register(Project)
class ProjectSerializer(Serializer):
    def serialize(self, obj, request=None):
        d = {
            'id': str(obj.id),
            'slug': obj.slug,
            'name': obj.name,
        }
        return d
