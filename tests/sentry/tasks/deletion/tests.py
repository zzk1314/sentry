# -*- coding: utf-8 -*-

from __future__ import absolute_import

from celery.task import Task
from sentry.models import (Team, Project, User)
from sentry.tasks.deletion import delete_object
from sentry.testutils import TestCase


class SentryCleanupTest(TestCase):
    def test_is_task(self):
        assert isinstance(delete_object, Task)

    def test_cascade(self):
    	user = User.objects.create(username='test')
    	team = Team.objects.create(owner=user, name='Test')
    	project = Project.objects.create(owner=user, team=team)
    	delete_object('sentry.models.User', user.id)
