from __future__ import absolute_import

__all__ = ('Analytics',)

import six

from sentry.utils.services import Service

from .event import Event
from .event_manager import default_manager


class Analytics(Service):
    __all__ = ('event', 'record', 'validate')

    event_manager = default_manager

    def event(self, event_type, **kwargs):
        """
        Return an Event instance. Useful for building up a partial event.

        For example, say you have an event which contains a 'previous' and
        'current' attribute:

        >>> event = analytics.event('organization.created', previous=organization)
        >>> organization.update(foo='bar')
        >>> analytics.record(event, current=organization)
        """
        event = self.event_manager.get(
            event_type,
        )
        return Event(
            type=event.type,
            attributes=event.attributes,
            **kwargs
        )

    def record(self, event_or_event_type, instance=None, **kwargs):
        """
        >>> analytics.record(Event())
        >>> analytics.record('organization.created', organization)
        """
        if isinstance(event_or_event_type, six.string_types):
            event = self.event_manager.get(
                event_or_event_type,
            ).from_instance(instance, **kwargs)
        else:
            event = event_or_event_type
        self.record_event(event)

    def record_event(self, event):
        """
        >>> analytics.record_event(Event())
        """

    def setup(self):
        # Load default event types
        import sentry.analytics.events  # NOQA
