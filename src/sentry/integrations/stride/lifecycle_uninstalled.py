from __future__ import absolute_import


from django.views.decorators.csrf import csrf_exempt

from sentry.api.base import Endpoint


class StrideUninstalledEndpoint(Endpoint):
    authentication_classes = ()
    permission_classes = ()

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(StrideUninstalledEndpoint, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Example payload:

        {
            key: 'sample-app',
            productType: 'chat',
            cloudId: 'xxx',
            resourceType: 'conversation',
            resourceId: 'yyy',
            eventType: 'uninstalled',
            userId: 'zzz',
            oauthClientId: 'aaa',
            version: '1'
        }
        """
        raise NotImplementedError
