
"""
sentry.access_groups.manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2013 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import, print_function, division

from django.core.context_processors import csrf
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.generic.base import View as BaseView

from sentry.models import Team, AccessGroup, AccessGroupOption
from sentry.web.helpers import success


class ConfigurationView(BaseView):
    def get_conf_key(self):
        raise NotImplementedError

    def get_form_class(self, request):
        raise NotImplementedError

    def render(self, request, template, context=None, **kwargs):
        from sentry.web.helpers import render_to_response

        if not context:
            context = {}

        if self.context:
            context.update(self.context)

        context.update(csrf(request))

        return render_to_response(self.template, context, request)

    def dispatch(self, request, team_slug, access_group_id, **kwargs):
        # TODO: handle invalid objects
        team = Team.objects.get_from_cache(slug=team_slug)
        access_group = AccessGroup.objects.get_from_cache(id=access_group_id)

        return super(ConfigurationView, self).dispatch(
            request=request,
            team=team,
            access_group=access_group,
            **kwargs
        )

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    @never_cache
    def get(self, request, team, access_group, **kwargs):
        config = AccessGroupOption.objects.get_value(
            access_group, self.get_conf_key(), {})

        form = self.get_form_class(request.POST or None, initial=config)
        if form.is_valid():
            AccessGroupOption.objects.set_value(
                access_group, self.get_conf_key(), form.cleaned_data)

            return success(request)

        return self.render(request, self.template, {
            'form': form,
        })


class AccessGroupManager(object):
    def __init__(self, group, config=None):
        self.group = group
        self.config = config or {}

    def get_conf_view(self):
        return ConfigurationView.as_view()

    def fetch_users(self):
        """
        Return a list User objects which are bound to this manager.
        """
        return []

    def sync(self):
        group = self.group
        users = set(self.fetch_users(group))

        # find existing members
        existing = set(group.members.all())

        # remove any users which no longer exist
        group.members.filter(id__in=existing - users).delete()

        # add our new members
        group.members.add(*list(users - existing))

        group.update(last_synced=timezone.now())


# TODO: support these in the extension system
from .ext.github import GitHubAccessGroupPlugin

EXTENSIONS = [
    GitHubAccessGroupPlugin,
]
