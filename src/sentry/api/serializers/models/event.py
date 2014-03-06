from sentry.api.serializers import Serializer, register
from sentry.models import Event


@register(Event)
class EventSerializer(Serializer):
    def serialize(self, obj, request=None):
        d = {
            'id': str(obj.id),
            'eventID': str(obj.event_id),
            'project': {
                'id': str(obj.project.id),
                'name': obj.project.name,
                'slug': obj.project.slug,
            },
            'message': obj.message,
            'culprit': obj.culprit,
            'checksum': obj.checksum,
            'platform': obj.platform,
            'dateCreated': self.localize_datetime(obj.datetime, request=request),
            'timeSpent': obj.time_spent,
        }
        return d
