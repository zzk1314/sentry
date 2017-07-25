from __future__ import absolute_import


def _import_all():
    __import__('sentry.grouping.strategies.generic')


_import_all()
del _import_all
