from __future__ import absolute_import

from .base import BaseEvent


class MonitorEvent(BaseEvent):
    key = 'monitor'

    def has_metadata(self):
        return 'sentry.interfaces.MonitorStatus' in self.data

    def get_metadata(self):
        print self.data
        cmd = self.data.get('sentry.interfaces.Command')
        status = self.data['sentry.interfaces.MonitorStatus']
        rv = {'status': status['status'], 'label': status['label']}
        if cmd:
            rv['executable'] = cmd['executable']
            rv['exit_code'] = cmd['exit_code']
        else:
            rv['executable'] = None
            rv['exit_code'] = None
        return rv

    def to_string(self, data):
        rv = '%s (%s)' % (data['label'], data['status'])
        if data['executable']:
            rv = '%s (exe=%s)' % (
                rv,
                data['executable'].rsplit('/', 1)[-1].rsplit('\\', 1)[-1]
            )
        if data['exit_code'] is not None:
            rv += '%s (exited with %s)' % (rv, data['exit_code'])
        return rv
