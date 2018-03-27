from __future__ import absolute_import

import uuid
import inspect
import itertools

from django.utils.functional import empty, LazyObject

from sentry.utils import warnings

from .imports import import_string


class Service(object):
    __all__ = ()

    def validate(self):
        """
        Validates the settings for this backend (i.e. such as proper connection
        info).

        Raise ``InvalidConfiguration`` if there is a configuration error.
        """

    def setup(self):
        """
        Initialize this service.
        """


class LazyServiceWrapper(LazyObject):
    """
    Lazyily instantiates a standard Sentry service class.

    >>> LazyServiceWrapper(BaseClass, 'path.to.import.Backend', {})

    Provides an ``expose`` method for dumping public APIs to a context, such as
    module locals:

    >>> service = LazyServiceWrapper(...)
    >>> service.expose(locals())
    """

    def __init__(self, backend_base, backend_path, options, dangerous=()):
        super(LazyServiceWrapper, self).__init__()
        self.__dict__.update(
            {
                '_backend': backend_path,
                '_options': options,
                '_base': backend_base,
                '_dangerous': dangerous,
            }
        )

    def __getattr__(self, name):
        if self._wrapped is empty:
            self._setup()
        return getattr(self._wrapped, name)

    def _setup(self):
        backend = import_string(self._backend)
        assert issubclass(backend, Service)
        if backend in self._dangerous:
            warnings.warn(
                warnings.UnsupportedBackend(
                    u'The {!r} backend for {} is not recommended '
                    'for production use.'.format(self._backend, self._base)
                )
            )
        instance = backend(**self._options)
        self._wrapped = instance

    def expose(self, context):
        base = self._base
        for key in itertools.chain(base.__all__, ('validate', 'setup')):
            if inspect.ismethod(getattr(base, key)):
                context[key] = (lambda f: lambda *a, **k: getattr(self, f)(*a, **k))(key)
            else:
                context[key] = getattr(base, key)


import time
from collections import OrderedDict
from functools import partial
from threading import Thread
from Queue import Queue
from concurrent.futures import Future

from sentry.utils.concurrent import FutureSet


class MultipleServiceBackend(object):
    def __init__(self, backends, methods, callback):
        self.backends = [(backend, self.__start_worker(backend)) for backend in backends]
        self.methods = methods
        self.callback = callback

    def __start_worker(self, backend):
        queue = Queue()

        def worker():
            while True:
                (name, args, kwargs), response = queue.get()
                if not response.set_running_or_notify_cancel():
                    continue

                start = time.time()
                method = getattr(backend, name)
                try:
                    result = True, method(*args, **kwargs)
                except Exception as error:
                    result = False, error

                response.set_result((
                    (start, time.time()),
                    result,
                ))

        t = Thread(target=worker)
        t.daemon = True
        t.start()

        def submit(request):
            response = Future()
            queue.put((request, response))
            return response

        return submit

    def __getattr__(self, name):
        if name not in self.methods:
            return getattr(self.backends[0][0], name)

        def execute(*args, **kwargs):
            request = (name, args, kwargs)

            responses = OrderedDict()
            for backend, submit in self.backends:
                responses[backend] = submit(request)

            callback = partial(self.callback, request, responses)
            FutureSet(responses.values()).add_done_callback(callback)

            timing, (success, result) = responses.values()[0].result()
            if success:
                return result
            else:
                raise result

        return execute
