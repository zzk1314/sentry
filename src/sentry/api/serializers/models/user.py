from sentry.api.serializers import Serializer, register
from sentry.models import User


@register(User)
class UserSerializer(Serializer):
    def serialize(self, obj, request=None):
        d = {
            'id': obj.id,
            'email': obj.email,
        }
        return d
