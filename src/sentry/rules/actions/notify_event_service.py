"""
sentry.rules.actions.notify_event_service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2014 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

from sentry.plugins import plugins
from sentry.rules.actions.base import EventAction
from sentry.utils.safe import safe_execute
from sentry.utils import metrics


class NotifyEventServiceAction(EventAction):
    label = 'Send a notification via {service}'

    def after(self, event, state):
        service = self.get_option('service')

        extra = {
            'event_id': event.id
        }
        if not service:
            self.logger.info('rules.fail.is_configured', extra=extra)
            return

        plugin = plugins.get(service)
        if not plugin.is_enabled(self.project):
            extra['project_id'] = self.project.id
            self.logger.info('rules.fail.is_enabled', extra=extra)
            return

        group = event.group

        if not plugin.should_notify(group=group, event=event):
            extra['group_id'] = group.id
            self.logger.info('rule.fail.should_notify', extra=extra)
            return

        metrics.incr('notifications.sent', instance=plugin.slug)
        yield self.future(plugin.rule_notify)

    def get_config(self):
        return [{
            'name': 'service',
            'type': 'choice',
            'choices': [(p.slug, p.get_title()) for p in self.get_plugins()],
            'required': True,
        }]

    def get_plugins(self):
        from sentry.plugins.bases.notify import NotificationPlugin

        results = []
        for plugin in plugins.for_project(self.project, version=1):
            if not isinstance(plugin, NotificationPlugin):
                continue
            results.append(plugin)

        for plugin in plugins.for_project(self.project, version=2):
            for notifier in (safe_execute(plugin.get_notifiers, _with_transaction=False) or ()):
                results.append(notifier)

        return results
