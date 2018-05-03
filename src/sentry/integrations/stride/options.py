from __future__ import absolute_import

from sentry.options import register, FLAG_PRIORITIZE_DISK

register('stride.client-id', flags=FLAG_PRIORITIZE_DISK)
register('stride.client-secret', flags=FLAG_PRIORITIZE_DISK)
