from __future__ import absolute_import

from django.db import models
from django.utils import timezone

from sentry.db.models import (
    BoundedBigIntegerField, FlexibleForeignKey, Model, sane_repr
)


class OrganizationStatType(Model):
    resolved_issues = 'resolved_issues'


class OrganizationStat(Model):
    organization = FlexibleForeignKey('sentry.Organization')
    stat = models.CharField(max_length=32)
    value = BoundedBigIntegerField()
    date = models.DateField(default=timezone.now)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_organizationstat'
        unique_together = (('organization', 'stat', 'date'),)

    __repr__ = sane_repr('organization', 'stat', 'date')
