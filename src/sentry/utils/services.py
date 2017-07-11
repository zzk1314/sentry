from __future__ import absolute_import

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


def build_lazy_method_wrapper(base, service, name):
    class LazyMethodDocumentationDescriptor(object):
        __slots__ = []

        def __get__(self, instance, owner):
            return getattr(service, name).__doc__

    class LazyMethodWrapper(object):
        __doc__ = LazyMethodDocumentationDescriptor()
        __slots__ = []
        __name__ = '<LazyMethodWrapper: {}.{}>'.format(base.__name__, name)

        def __repr__(self):
            return '<{}: {}.{}>'.format(type(self).__name__, service, name)

        def __call__(self, *args, **kwargs):
            return getattr(service, name)(*args, **kwargs)

    return LazyMethodWrapper()


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
        self.__dict__.update({
            '_backend': backend_path,
            '_options': options,
            '_base': backend_base,
            '_dangerous': dangerous,
        })

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
                context[key] = build_lazy_method_wrapper(base, self, key)
            else:
                context[key] = getattr(base, key)
