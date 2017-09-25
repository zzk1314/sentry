from __future__ import absolute_import

from sentry.integrations import NotificationProvider


class SlackNotificationProvider(NotificationProvider):
    def get_config(self):
        return [{
            'name': 'route',
            'required': True,
            'placeholder': '#general'
        }]

    def get_types(self):
        return [NotificationType.alert]

    def send(self, event):
        pass
