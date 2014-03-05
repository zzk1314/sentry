from sentry.api.serializers import Serializer, register
from sentry.models import PendingTeamMember


@register(PendingTeamMember)
class PendingTeamMemberSerializer(Serializer):
    def serialize(self, obj, request=None):
        d = {
            'id': str(obj.id),
            'email': obj.email,
            'access': obj.get_type_display(),
            'pending': True,
            'dateAdded': obj.date_added,
        }
        return d
