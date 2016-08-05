from __future__ import absolute_import

import base64
from uuid import uuid4

from django.db import models
from django.utils import timezone

from sentry.db.models import Model, FlexibleForeignKey, sane_repr, \
    BaseManager, GzippedDictField
from sentry.utils.numbers import base32_decode, base32_encode
from sentry.utils.http import absolute_uri


class MonitorManager(BaseManager):

    def get_from_token(self, token):
        if '.' not in token:
            raise Monitor.DoesNotExist()
        manager_id, manager_secret = token.split('.', 1)
        try:
            manager_id = base32_decode(manager_id)
        except ValueError:
            raise Monitor.DoesNotExist()
        rv = self.get(pk=manager_id)
        if rv.secret_key != manager_secret:
            raise Monitor.DoesNotExist()
        return rv


class Monitor(Model):
    __core__ = True

    objects = MonitorManager()

    project = FlexibleForeignKey('sentry.Project')
    label = models.CharField(max_length=64, blank=True, null=True)
    secret_key = models.CharField(max_length=32, unique=True, null=True)
    date_added = models.DateTimeField(default=timezone.now, null=True)

    status = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    metadata = GzippedDictField()

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_monitors'

    __repr__ = sane_repr('project_id', 'label')

    def save(self, *args, **kwargs):
        if not self.secret_key:
            self.secret_key = uuid4().hex
        Model.save(self, *args, **kwargs)

    @property
    def is_healthy(self):
        return self.status == 0

    @property
    def is_running(self):
        return self.status == -1

    @property
    def token(self):
        return '%s.%s' % (
            base32_encode(self.id).lower(),
            self.secret_key,
        )

    @property
    def full_token(self):
        return base64.b64encode(self.get_api_url()).strip('=')

    def get_api_url(self):
        return absolute_uri('/api/0/monitors/%s/' % self.token)

    def start_job(self, timestamp, command=None, args=None):
        self.started_at = timestamp
        self.finished_at = None
        self.metadata = {
            'command': command,
            'args': args,
            'output': None,
        }
        self.save()

    def complete_job(self, timestamp, status=None, output=None):
        self.finished_at = timestamp
        self.status = status or 0
        self.metadata['output'] = output
        self.save()

        if self.status == 0:
            return

        # Needs to be local imports because reasons
        from sentry.event_manager import EventManager

        data = {
            'timestamp': timestamp,
            'type': 'monitor',
            'level': 'error',
            'sentry.interfaces.Command': {
                'executable': self.metadata['command'],
                'exit_code': self.status,
                'args': self.metadata['args'],
                'output': self.metadata['output'],
            },
            'sentry.interfaces.MonitorStatus': {
                'monitor_id': str(self.id),
                'label': self.label,
                'status': 'failed',
            }
        }

        mgr = EventManager(data)
        mgr.normalize()
        mgr.save(self.project_id)
