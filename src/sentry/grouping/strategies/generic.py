from __future__ import absolute_import

from sentry.grouping.strategies.api import Strategy, register_strategy


@register_strategy(
    identifier='generic-exception',
    flavors=['platform:generic'],
    priority=100,
    version='1.0',
)
class GenericExceptionStrategy(Strategy):

    @classmethod
    def is_applicable_for_data(cls, data):
        return 'sentry.interfaces.Exception' in data
