from __future__ import absolute_import

from sentry.api.base import Endpoint
from sentry.utils.http import absolute_uri

from .client import BITBUCKET_KEY
from sentry.integrations.bitbucket.integration import scopes


class BitbucketDescriptorEndpoint(Endpoint):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        return self.respond(
            {
                'key': BITBUCKET_KEY,
                'name': 'Sentry for Bitbucket',
                'description': 'A Sentry integration',
                'vendor': {
                    'name': 'Sentry.io',
                    'url': 'https://sentry.io/'
                },
                'baseUrl': absolute_uri(),
                'authentication': {
                    'type': 'JWT',
                },
                'lifecycle': {
                    'installed': '/extensions/bitbucket/installed/',
                    'uninstalled': '/extensions/bitbucket/uninstalled/'
                },
                'scopes': scopes,
                'contexts': ['account'],
                'modules': {
                    'postInstallRedirect': {
                        # from depricated example here: https://developer.atlassian.com/cloud/bitbucket/modules/post-install-redirect/
                        'key': 'redirect',
                        'url': '/extensions/bitbucket/installed?user={user_username}/'  # is this the idea? to give context to the intalled endpoint?
                        # ????
                        # user.username
                        # user.uuid
                        # user. (etc)
                        # target_user.username
                        # target_user.uuid
                        # target_user. (etc)
                        # where user is the authenticated user and target_user is the account into which the app is installed (could be a team or a personal account)
                    }
                }
            }
        )
