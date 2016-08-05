from __future__ import absolute_import

from sentry.api.serializers import register, serialize, Serializer
from sentry.models import Monitor


@register(Monitor)
class MonitorSerializer(Serializer):

    def serialize(self, obj, attrs, user):
        return {
            'id': str(obj.id),
            'label': obj.label,
            'status': obj.status,
            'isActive': obj.is_active,
            'startedAt': obj.started_at,
            'finishedAt': obj.finished_at,
            'dateAdded': obj.date_added,
            'metadata': obj.metadata,
            'project': serialize(obj.project),
        }
