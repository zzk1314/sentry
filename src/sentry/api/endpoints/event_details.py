from rest_framework.response import Response

from sentry.api.base import Endpoint
from sentry.api.serializers import serialize
from sentry.models import Event


class EventDetailsEndpoint(Endpoint):
    def get(self, request, event_id):
        event = Event.objects.get(
            id=event_id
        )

        base_qs = Event.objects.filter(
            group=event.group_id,
        ).exclude(id=event.id)
        try:
            next_event = base_qs.filter(datetime__gte=event.datetime).order_by('datetime')[0:1].get()
        except Event.DoesNotExist:
            next_event = None

        try:
            prev_event = base_qs.filter(datetime__lte=event.datetime).order_by('-datetime')[0:1].get()
        except Event.DoesNotExist:
            prev_event = None

        data = serialize(event, request)

        if next_event:
            data['nextEventID'] = str(next_event.id)
        else:
            data['nextEventID'] = None
        if prev_event:
            data['previousEventID'] = str(prev_event.id)
        else:
            data['previousEventID'] = None

        return Response(data)
