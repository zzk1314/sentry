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


import functools
import time
import thread

from sentry.utils.concurrent import FutureSet


class MultipleServiceBackend(object):
    def __init__(self, executor, backends, methods, callback):
        self.__uuid = uuid.uuid1()
        self.executor = executor
        self.backends = backends
        self.methods = methods
        self.callback = callback

    def __getattr__(self, name):
        if name not in self.methods:
            return getattr(self.backends[0], name)

        def execute_and_time(backend, name, *args, **kwargs):
            start = time.time()
            try:
                method = getattr(backend, name)
                result = True, method(*args, **kwargs)
            except Exception as error:
                result = False, error
            return '{}/{}'.format(self.__uuid.hex, thread.get_ident()), backend, start, time.time(), result

        def execute(*args, **kwargs):
            futures = []
            for backend in self.backends:
                future = self.executor.submit(execute_and_time, backend, name, *args, **kwargs)
                futures.append(future)

            FutureSet(futures).add_done_callback(functools.partial(self.callback, name, args, kwargs))

            _, _, start, stop, (success, response) = futures[0].result()
            if not success:
                raise response

            return response

        return execute
