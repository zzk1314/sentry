from __future__ import absolute_import

from .base import *  # NOQA
from .manager import IntegrationManager  # NOQA
from .oauth import *  # NOQA
from .view import *  # NOQA

# TODO(dcramer): pull these into the integrations namespace
from sentry.plugins.providers.notification import NotificationProvider
from sentry.plugins.providers.repository import RepositoryProvider


default_manager = IntegrationManager()
all = default_manager.all
get = default_manager.get
exists = default_manager.exists
register = default_manager.register
unregister = default_manager.unregister
