import logging
from functools import partial
from string import Formatter
from time import time

class dontexplodedict(object):
    """
    A dictionary that won't throw a KeyError and will
    return back a sensible default value to be used in
    string formatting.
    """
    def __init__(self, d=None):
        self.data = d or {}

    def __getitem__(self, key):
        # We're explicitly mutating and popping
        # off keys so they can't be reused. This
        # allows us to get unused keys.
        return self.data.pop(key, '')


class Message(object):
    __counter = 0
    __registry = {}

    def __init__(self, message):
        cls = type(self)
        if type(message) == str:
            message = message.decode('utf8')
        self.id = cls.__counter
        cls.__registry[self.id] = message
        cls.__counter += 1

    @classmethod
    def get(cls, id, data):
        try:
            return Formatter().vformat(
                cls.__registry[id],
                [],
                dontexplodedict(data),
            )
        except KeyError:
            return '<unknown>'

M = Message


def ts():
    "timestamp in milliseconds"
    return int(time() * 1000)


class EventLogger(object):
    def __init__(self, data, logger=None):
        self.data = data
        self.logger = logger

    def log(self, level, message, **kwargs):
        if kwargs:
            self.data['log'].append((ts(), level, message.id, kwargs))
        else:
            self.data['log'].append((ts(), level, message.id))

    def debug(self, message, **kwargs):
        self.log(logging.DEBUG, message, **kwargs)

    def info(self, message, **kwargs):
        self.log(logging.INFO, message, **kwargs)


def bind(data):
    if 'log' not in data:
        data['log'] = []
    return EventLogger(data)


def getMessage((ts, level, message, data)):
    return {
        'ts': ts,
        'level': logging.getLevelName(level),
        'message': Message.get(message, data),
        'extra': data,
    }


API_SCRUB_IP_ORGANIZATION = M('api: scrubbing IP due to organization settings')
API_SCRUB_IP_PROJECT = M('api: scrubbing IPs due to project settings')
API_SCRUB_DATA_ORGANIZAITON = M('api: scrubbing data due to organization settings')
API_SCRUB_DATA_PROJECT = M('api: scrubbing data due to project settings')

JS_PROCESSOR_CHECKING_RELEASEFILE = M('js_processor: checking cache for {filename!r} in release {release!r}')
