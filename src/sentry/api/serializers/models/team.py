from sentry.api.serializers import Serializer, register
from sentry.models import Team


@register(Team)
class TeamSerializer(Serializer):
    def serialize(self, obj, request=None):
        d = {
            'id': str(obj.id),
            'slug': obj.slug,
            'name': obj.name,
            'dateAdded': obj.date_added,
        }
        return d
