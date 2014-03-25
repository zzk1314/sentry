from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from rest_framework.response import Response

from sentry.api.authentication import QuietBasicAuthentication
from sentry.api.base import Endpoint


class AuthIndexEndpoint(Endpoint):
    authentication_classes = [QuietBasicAuthentication]

    def post(self, request):
        if not request.user.is_authenticated():
            return Response(status=400)

        login(request, request.user)
        return HttpResponseRedirect(reverse('sentry-api-0-user-details', args=[request.user.id]))

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=204)
