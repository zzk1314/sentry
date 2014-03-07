from django.db.models.signals import post_save

from sentry.app import pubsub
from sentry.api.serializers import serialize
from sentry.models import Group
from sentry.utils import json


def get_group_channels(group):
    return [
        'project:{0}:groups'.format(group.project_id),
    ]


def publish_group_update(instance, **kwargs):
    data = json.dumps(serialize(instance))

    for channel in get_group_channels(instance):
        pubsub.publish(channel, {
            'data': data,
            'event': 'group.update',
        })


post_save.connect(
    publish_group_update,
    sender=Group,
    dispatch_uid="publish_group_update",
    weak=False,
)
