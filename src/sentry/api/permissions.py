from django_sudo.utils import has_sudo_privileges

from sentry.constants import MEMBER_USER
from sentry.models import Team, Project, User


class ElevatedAuthenticationRequired(Exception):
    pass


class PermissionError(Exception):
    pass


def has_perm(object, user, access=MEMBER_USER):
    if user.is_superuser:
        return True

    # TODO: abstract this into a permission registry
    if type(object) == User:
        return object == user

    if type(object) == Team:
        return object.slug in Team.objects.get_for_user(user, access=access)

    if hasattr(object, 'project'):
        object = object.project

    if type(object) == Project:
        return object.slug in Project.objects.get_for_user(user, access=access)

    raise TypeError(type(object))


def assert_perm(*args, **kwargs):
    if not has_perm(*args, **kwargs):
        raise PermissionError


def assert_sudo(request):
    # TODO(dcramer): what should this do when its called via an API token?
    # should it just not be usable?
    if not has_sudo_privileges(request):
        raise ElevatedAuthenticationRequired
