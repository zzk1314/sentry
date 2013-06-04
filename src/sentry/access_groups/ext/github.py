"""
sentry.access_groups.ext.github
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2013 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from django import forms
from django.utils.translation import ugettext_lazy as _

from sentry.access_groups.base import AccessGroupManager, ConfigurationView


class GitHubConfigurationView(ConfigurationView):
    # TODO: validate
    org = forms.CharField(label=_('Organization Name'),
        widget=forms.TextInput(attrs={'placeholder': 'e.g. getsentry'}),
        help_text=_('Enter your organization name.'))


class GitHubAccessGroupManager(AccessGroupManager):
    # TODO: currently assumes that the team owner has associated their
    # github account
    def get_conf_key(self):
        return 'github:access_group'

    def get_conf_view(self):
        return GitHubConfigurationView.as_view()

    def fetch_users(self):
        """
        Return a list User objects which are bound to this access group.
        """
        return []
