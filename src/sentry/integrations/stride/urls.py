from __future__ import absolute_import, print_function

from django.conf.urls import patterns, url

from .lifecycle_installed import StrideInstalledEndpoint
from .lifecycle_uninstalled import StrideUninstalledEndpoint
from .descriptor import StrideDescriptorEndpoint


urlpatterns = patterns(
    '',
    url(r'^lifecycle/installed/$', StrideInstalledEndpoint.as_view()),
    url(r'^lifecycle/uninstalled/$', StrideUninstalledEndpoint.as_view()),
    url(r'^descriptor/$', StrideDescriptorEndpoint.as_view()),
)
