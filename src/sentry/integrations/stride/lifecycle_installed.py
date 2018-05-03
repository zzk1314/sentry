from __future__ import absolute_import


from django.db import IntegrityError, transaction
from django.views.decorators.csrf import csrf_exempt

from sentry.api.base import Endpoint
from sentry.models import Integration


class StrideInstalledEndpoint(Endpoint):
    authentication_classes = ()
    permission_classes = ()

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(StrideInstalledEndpoint, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Example payload:

        {
            key: 'sample-app',
            productType: 'chat',
            cloudId: 'xxx',
            resourceType: 'conversation',
            resourceId: 'yyy',
            eventType: 'installed',
            userId: 'zzz',
            oauthClientId: 'aaa',
            version: '1'
        }
        """
        data = request.DATA
        # TODO(dcramer): Handle updating existing integration
        try:
            with transaction.atomic():
                Integration.objects.create(
                    provider='stride',
                    external_id=data['cloudId'],
                    name=data['key'],
                    metadata={
                        'oauth_client_id': data['oauthClientId'],
                        'cloud_id': data['cloudId'],
                    }
                )
        except IntegrityError:
            pass

        return self.respond()
