from __future__ import absolute_import

from enum import Enum

from .base import ProviderMixin


class NotificationType(Enum):
    # TODO(dcramer): make these references to the base class of the event type?
    alert = 'alert'


class NotificationProvider(ProviderMixin):
    def __init__(self, integration_config):
        # instance of <IntegrationConfig>
        self.integration_config = integration_config

    def get_config(self):
        return []

    def get_types(self):
        raise NotImplementedError

    def send(self, event):
        raise NotImplementedError
