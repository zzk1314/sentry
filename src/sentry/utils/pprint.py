"""
sentry.utils.pprint
~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2012 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import


def pformat(instance, depth=0):
    """Format a Python object into a pretty-printed representation."""
    if isinstance(instance, (list, tuple, set, frozenset)):
        out = '['
        num_items = len(instance)
        for num, item in enumerate(instance):
            if num > 5:
                out += ' ... %s more items' % (num_items - num,)
                break
            if num == num_items - 1:
                out += pformat(item, depth=depth + 1)
            else:
                out += '%s, ' % (pformat(item, depth=depth + 1))
        out += ']\n'
    elif isinstance(instance, dict):
        out = '{'
        num_items = len(instance)
        for num, (key, value) in enumerate(instance.iteritems()):
            if num > 5:
                out += ' ... %s more items' % (num_items - num,)
                break
            if num_items > 5:
                out += '\n    '
            out += '%s => %s' % (key, pformat(value, depth=depth + 1))
        if num_items > 5:
            out += '\n'
        out += '}'
    else:
        out = unicode(instance)

    return out
