from __future__ import absolute_import, print_function

__all__ = ('Attribute', 'Event', 'Map')

import six

from collections import Mapping
from django.utils import timezone


class Attribute(object):
    def __init__(self, name, type=six.text_type, required=True):
        self.name = name
        self.type = type
        self.required = required

    def extract(self, value):
        if value is None:
            return value
        return self.type(value)


class Map(Attribute):
    def __init__(self, name, attributes=None, required=True):
        self.name = name
        self.required = required
        self.attributes = attributes

    def extract(self, value):
        """
        If passed a non dictionary we assume we can pull attributes from it.

        This will hard error in some situations if you're passing a bad type
        (like an int).
        """
        if value is None:
            return value

        if not isinstance(value, Mapping):
            new_value = {}
            for attr in self.attributes:
                new_value[attr.name] = attr.extract(
                    getattr(value, attr.name, None)
                )
            items = new_value
        else:
            # ensure we dont mutate the original
            # we dont need to deepcopy as if it recurses into another Map it
            # will once again copy itself
            items = value.copy()

        data = {}
        for attr in self.attributes:
            nv = items.pop(attr.name, None)
            if attr.required and nv is None:
                raise ValueError(u'{} is required (cannot be None)'.format(
                    attr.name,
                ))

            data[attr.name] = attr.extract(nv)

        if items:
            raise ValueError(u'Unknown attributes: {}'.format(
                ', '.join(map(six.text_type, six.iterkeys(items))),
            ))

        return data


class Event(object):
    __slots__ = ['attributes', 'data', 'datetime', 'type']

    data = None

    type = None

    attributes = ()

    def __init__(self, type=None, datetime=None, attributes=None, **items):
        self.datetime = datetime or timezone.now()
        if type is not None:
            self.type = type

        if self.type is None:
            raise ValueError('Event is missing type')

        if attributes is not None:
            self.attributes = attributes

        data = {}
        for attr in self.attributes:
            nv = items.pop(attr.name, None)
            data[attr.name] = attr.extract(nv)

        if items:
            raise ValueError(u'Unknown attributes: {}'.format(
                ', '.join(six.iterkeys(items)),
            ))

        self.data = data

    def __setattr__(self, name, value):
        # yeah, this is slow
        # yeah, we'll fix it later
        if name in ('data', 'datetime', 'type', 'attributes'):
            return super(Event, self).__setattr__(name, value)

        for attr in self.attributes:
            if attr.name == name:
                self.data[name] = attr.extract(value)
                return

        raise AttributeError(u'Unknown attribute: {}'.format(
            name,
        ))

    def __getattr__(self, name):
        # yeah, this is slow
        # yeah, we'll fix it later
        for attr in self.attributes:
            if attr.name == name:
                return self.data.get(name)

        raise AttributeError(u'Unknown attribute: {}'.format(
            name,
        ))

    def validate(self):
        for attr in self.attributes:
            value = self.data.get(attr.name)
            if attr.required and value is None:
                raise ValueError(u'{} is required (cannot be None)'.format(
                    attr.name,
                ))

    def serialize(self):
        self.validate()
        return dict({
            'timestamp': int(self.datetime.isoformat('%s')),
            'type': self.type,
        }, **self.data)

    @classmethod
    def from_instance(cls, instance, **kwargs):
        values = {}
        for attr in cls.attributes:
            values[attr.name] = (
                kwargs.get(attr.name) or
                getattr(instance, attr.name, None)
            )
        return cls(**values)
