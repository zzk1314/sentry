from __future__ import absolute_import

__all__ = ('MonitorStatus',)

from sentry.interfaces.base import Interface, InterfaceValidationError
from sentry.utils.safe import trim


STATUS_SET = frozenset([
    'healthy',
    'failed',
    'missed',
])


class MonitorStatus(Interface):
    """
    An interface which describes the status of a monitor.
    """

    @classmethod
    def to_python(cls, data):
        try:
            if data['status'] not in STATUS_SET:
                raise InterfaceValidationError(
                    'Invalid status: %s' % data['status'])
        except KeyError:
            raise InterfaceValidationError('Missing status')

        monitor_id = data.get('monitor_id')
        if not isinstance(monitor_id, basestring):
            raise InterfaceValidationError('Invalid monitor ID')

        return cls(
            monitor_id=trim(monitor_id, 100),
            label=trim(data.get('label'), 255),
            status=data['status'],
        )

    def get_api_context(self, is_public=False):
        return {
            'monitorId': self.monitor_id,
            'label': self.label,
            'status': self.status,
        }

    def get_path(self):
        return 'sentry.interfaces.MonitorStatus'

    def get_hash(self):
        return [self.monitor_id, self.status]
