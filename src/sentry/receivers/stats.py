from __future__ import absolute_import

from sentry.signals import issues_resolved



issues_resolved.connect(
    record_instance_creation,
    weak=False,
    dispatch_uid='sentry.stats.tasks.record_instance_creation',
)
