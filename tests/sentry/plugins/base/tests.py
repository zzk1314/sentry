# -*- coding: utf-8 -*-

from __future__ import absolute_import

from sentry.plugins.base import Plugin
from sentry.testutils import TestCase


class DummyPluginWithUrls(Plugin):
    urls_app_name = 'dummy'
    urls_name = 'dummy'

    def get_urls(self):
        """
        Returns a urlpatterns object.

        Views (unless otherwise nescesary) should be decorated via ``self.as_view(callable)``
        within the urlpatterns.
        """
        from django.conf.urls.defaults import patterns, url

        urlpatterns = patterns('',
            url(r'^one/$', self.as_view(self.view_one)),
            url(r'^two/$', self.as_view(self.view_one)),
        )

        return urlpatterns

    def view_one(self):
        return self.render('view_one.html')

    def view_two(self):
        return self.render('view_two.html')


# class SentryPluginTest(TestCase):
#     def test_does_manage_urls(self):
#         return ''
#     