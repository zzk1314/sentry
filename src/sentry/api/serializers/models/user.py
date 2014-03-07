from sentry.api.serializers import Serializer, register
from sentry.models import User


@register(User)
class UserSerializer(Serializer):
    def serialize(self, obj, user):
        d = {
            'id': str(obj.id),
            'email': obj.email,
        }
        return d
