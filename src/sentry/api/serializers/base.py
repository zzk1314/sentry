from sentry.app import env
from sentry.utils import json


serializers = {}


def serialize(objects, request=None):
    if request is None:
        request = getattr(env, 'request', None)
    if not objects:
        return objects
    elif not isinstance(objects, (list, tuple)):
        return serialize([objects], request=request)[0]

    # elif isinstance(obj, dict):
    #     return dict((k, serialize(v, request=request)) for k, v in obj.iteritems())
    try:
        t = serializers[type(objects[0])]
    except KeyError:
        return objects

    t.attach_metadata(objects, request=request)
    return [t(o, request=request) for o in objects]


def to_json(obj, request=None):
    result = serialize(obj, request=request)
    return json.dumps(result)


def register(type):
    def wrapped(cls):
        serializers[type] = cls()
        return cls
    return wrapped


class Serializer(object):
    def __call__(self, obj, request=None):
        return self.serialize(obj, request)

    def attach_metadata(self, objects, request=None):
        pass

    def serialize(self, obj, request=None):
        return {}

    def localize_datetime(self, dt, request=None):
        if not request:
            return dt.isoformat()
        elif getattr(request, 'timezone', None):
            return dt.astimezone(request.timezone).isoformat()
        return dt.isoformat()
