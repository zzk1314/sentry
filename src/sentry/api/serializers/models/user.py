from sentry.api.serializers import Serializer, register
from sentry.models import User


@register(User)
class UserSerializer(Serializer):
    def serialize(self, obj, user):
        d = {
            'id': str(obj.id),
            'name': obj.get_full_name(),
            'email': obj.email,
        }
        return d
