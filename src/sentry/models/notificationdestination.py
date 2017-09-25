from __future__ import absolute_import

from django.db import models, IntegrityError, transaction
from jsonfield import JSONField

from sentry.db.models import FlexibleForeignKey, Model


class NotificationDestination(Model):
    __core__ = False

    organization = FlexibleForeignKey('sentry.Organization')
    integration = FlexibleForeignKey('sentry.Integration')
    name = models.CharField(max_length=200)
    config = JSONField(default=lambda: {})

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_notificationdestination'
        unique_together = (('organization', 'integration', 'name'),)
