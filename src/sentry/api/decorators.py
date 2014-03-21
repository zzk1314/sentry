from django.http import HttpResponse
from django_sudo.utils import has_sudo_privileges
from functools import wraps


def sudo_required(func):
    @wraps(func)
    def wrapped(self, request, *args, **kwargs):
        if not has_sudo_privileges(request):
            # TODO(dcramer): support some kind of auth flow to allow this
            # externally
            return HttpResponse(
                content='Account verification required',
                status=401,
            )
        return func(self, request, *args, **kwargs)
    return wrapped
