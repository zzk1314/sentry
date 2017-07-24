from __future__ import absolute_import

import posixpath

from sentry.grouping.strategies.api import Strategy, register_strategy


@register_strategy(
    identifier='generic-in-app-exception',
    flavors=['platform:generic'],
    priority=100,
    version='1.0',
)
@register_strategy(
    identifier='generic-exception',
    flavors=['platform:generic'],
    priority=110,
    version='1.0',
)
class GenericExceptionStrategy(Strategy):
    interfaces = [
        'sentry.interfaces.Exception',
    ]

    @property
    def stracktrace_strategy_id(self):
        if self.version.identifier == 'generic-in-app-exception':
            return 'generic-in-app-stacktrace'
        return 'generic-system-stacktrace'

    @classmethod
    def is_applicable_for_data(cls, data):
        return bool(
            'sentry.interfaces.Exception' in data and
            data['sentry.interfaces.Exception'].get('values'))

    def hash_interfaces(self, interfaces, platform, hasher):
        exc = interfaces['sentry.interfaces.Exception']
        for value in exc.values:
            if not value.stacktrace:
                continue
            hasher.contribute_nested(
                identifier=self.stracktrace_strategy_id,
                preferred_version='latest',
                interfaces={
                    'sentry.interfaces.Stacktrace': value.stacktrace,
                }
            )


@register_strategy(
    identifier='generic-in-app-stacktrace',
    flavors=['platform:generic'],
    priority=200,
    version='1.0',
)
@register_strategy(
    identifier='generic-system-stacktrace',
    flavors=['platform:generic'],
    priority=210,
    version='1.0',
)
class GenericStacktraceStrategy(Strategy):
    interfaces = [
        'sentry.interfaces.Stacktrace',
    ]

    @classmethod
    def is_applicable_for_data(cls, data):
        return 'sentry.interfaces.Stacktrace' in data

    def get_relevant_frames(self, frames, platform):
        if not frames:
            return []

        if self.identifier == 'generic-system-stacktrace':
            total_frames = len(frames)
            frames = [f for f in frames if f.in_app] or frames

            # if app frames make up less than 10% of the stacktrace discard
            # the hash as invalid
            if len(frames) / float(total_frames) < 0.10:
                return []

        return frames

    def can_use_context_line(self, frame, platform):
        if frame.context_line is None:
            return False
        elif len(frame.context_line) > 120:
            return False
        elif self.function:
            return True
        return False

    def remove_filename_outliers(self, filename, platform):
        return posixpath.basename(filename)

    def hash_frame(self, frame, platform, hasher):
        platform = frame.platform or platform

        if frame.module:
            hasher.contribute_value(frame.module)
        elif frame.filename:
            hasher.contribute_value(self.remove_filename_outliers(
                frame.filename, platform))

        if self.can_use_context_line(frame, platform):
            hasher.contribute_value(frame.context_line.strip())

        if not hasher.did_contribute:
            return
        elif frame.symbol:
            hasher.contribute_value(frame.symbol)
        elif frame.function:
            hasher.contribute_value(frame.function)

    def hash_interfaces(self, interfaces, platform, hasher):
        stacktrace = interfaces['sentry.interfaces.Stacktrace']
        frames = stacktrace.frames

        # Do not hash empty stacktraces
        if not frames:
            return

        first_frame = frames[0]
        stack_invalid = (
            len(frames) == 1 and
            (first_frame.platform or platform) == 'javascript' and
            first_frame.function and
            first_frame.is_url()
        )

        if stack_invalid:
            return

        for frame in self.get_relevant_frames(frames, platform):
            self.hash_frame(frame, platform, hasher)
