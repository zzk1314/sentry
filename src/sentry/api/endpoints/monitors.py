import time

from rest_framework.response import Response

from sentry.api.base import Endpoint
from sentry.api.serializers import serialize
from sentry.models import Monitor
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.utils.dates import to_datetime


class MonitorEndpoint(Endpoint):
    authentication_classes = ()
    permission_classes = ()

    def convert_args(self, request, monitor_token, *args, **kwargs):
        try:
            monitor = Monitor.objects.get_from_token(monitor_token)
        except Monitor.DoesNotExist:
            raise ResourceDoesNotExist()
        kwargs['monitor'] = monitor
        return (args, kwargs)


class StartMonitorEndpoint(MonitorEndpoint):

    def post(self, request, monitor):
        monitor.start_job(
            timestamp=to_datetime(request.DATA.get('timestamp') or time.time()),
            command=request.DATA.get('command'),
            args=request.DATA.get('args'),
        )
        return Response(serialize(monitor))


class CompleteMonitorEndpoint(MonitorEndpoint):

    def post(self, request, monitor):
        monitor.complete_job(
            timestamp=to_datetime(request.DATA.get('timestamp') or time.time())
        )
        return Response(serialize(monitor))


class FailMonitorEndpoint(MonitorEndpoint):

    def post(self, request, monitor):
        monitor.complete_job(
            status=request.DATA.get('status') or 255,
            timestamp=to_datetime(request.DATA.get('timestamp') or time.time()),
            output=request.DATA.get('output')
        )
        return Response(serialize(monitor))
