from __future__ import absolute_import

from sentry.grouping.strategies.api import Strategy, register_strategy


@register_strategy(
    identifier='generic-exception',
    flavors=['platform:generic'],
    priority=100,
    version='1.0',
)
class GenericExceptionStrategy(Strategy):
    interfaces = [
        'sentry.interfaces.Exception',
    ]

    @classmethod
    def is_applicable_for_data(cls, data):
        return bool(
            'sentry.interfaces.Exception' in data and
            data['sentry.interfaces.Exception'].get('values'))

    def hash_interfaces(self, interfaces, platform, hasher):
        exc = interfaces[0]
        for stacktrace in exc.values:
            hasher.contribute_nested(
                identifier='generic-stacktrace',
                preferred_version='latest',
                interfaces=[stacktrace]
            )


@register_strategy(
    identifier='generic-stacktrace',
    flavors=['platform:generic'],
    priority=200,
    version='1.0',
)
class GenericStacktraceStrategy(Strategy):
    interfaces = [
        'sentry.interfaces.Stacktrace',
    ]

    @classmethod
    def is_applicable_for_data(cls, data):
        return 'sentry.interfaces.Stacktrace' in data

    def hash_interfaces(self, interfaces, platform, hasher):
        stacktrace = interfaces[0]

        # Do not hash empty stacktraces
        if not stacktrace.frames:
            return

        first_frame = stacktrace.frames[0]
        stack_invalid = (
            len(stacktrace.frames) == 1 and
            (first_frame.platform or platform) == 'javascript' and
            first_frame.function and
            first_frame.is_url()
        )

        if stack_invalid:
            return
