from __future__ import absolute_import

from six.moves.urllib.parse import urlparse

from sentry.api.base import Endpoint
from sentry.utils.http import absolute_uri


STRIDE_KEY = '%s.stride' % (urlparse(absolute_uri()).hostname, )


class StrideDescriptorEndpoint(Endpoint):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        return self.respond(
            {
                'name': 'Sentry',
                'description': 'Sentry',
                'key': STRIDE_KEY,
                'baseUrl': absolute_uri(),
                'vendor': {
                    'name': 'Sentry',
                    'url': 'https://sentry.io'
                },
                'authentication': {
                    'type': 'jwt'
                },
                'lifecycle': {
                    'installed': '/extensions/stride/lifecycle/installed/',
                    'uninstalled': '/extensions/stride/lifecycle/uninstalled/',
                },
                'apiVersion': 1,
                'modules': {
                    # 'configurePage': {
                    #     'url': '/extensions/stride/configure',
                    #     'name': {
                    #         'value': 'Configure Sentry Add-on'
                    #     },
                    #     'key': 'configure-sentry'
                    # },
                },
                # 'scopes': [
                #     'read',
                #     'write',
                #     'act_as_user',
                # ]
            }
        )
