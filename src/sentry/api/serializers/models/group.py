from collections import defaultdict
from django.core.urlresolvers import reverse

from sentry.api.serializers import Serializer, register
from sentry.constants import STATUS_RESOLVED, STATUS_MUTED, TAG_LABELS
from sentry.models import (
    Group, GroupBookmark, GroupTagKey, GroupSeen, ProjectOption
)
# from sentry.templatetags.sentry_plugins import get_tags
# from sentry.templatetags.sentry_plugins import handle_before_events
from sentry.utils.db import attach_foreignkey
from sentry.utils.http import absolute_uri


@register(Group)
class GroupSerializer(Serializer):
    def get_attrs(self, item_list, user):
        attach_foreignkey(item_list, Group.project, ['team'])

        # if request and objects:
        #     handle_before_events(request, objects)

        if user.is_authenticated() and item_list:
            bookmarks = set(GroupBookmark.objects.filter(
                user=user,
                group__in=item_list,
            ).values_list('group_id', flat=True))
            seen_groups = dict(GroupSeen.objects.filter(
                user=user,
                group__in=item_list,
            ).values_list('group_id', 'last_seen'))
        else:
            bookmarks = set()
            seen_groups = {}

        project_list = set(o.project for o in item_list)
        tag_keys = set(['sentry:user'])
        project_annotations = {}
        for project in project_list:
            enabled_annotations = ProjectOption.objects.get_value(
                project, 'annotations', ['sentry:user'])
            project_annotations[project] = enabled_annotations
            tag_keys.update(enabled_annotations)

        annotation_counts = defaultdict(dict)
        annotation_results = GroupTagKey.objects.filter(
            group__in=item_list,
            key__in=tag_keys,
        ).values_list('key', 'group', 'values_seen')
        for key, group_id, values_seen in annotation_results:
            annotation_counts[key][group_id] = values_seen

        result = {}
        for item in item_list:
            active_date = item.active_at or item.last_seen

            annotations = {}
            for key in sorted(tag_keys):
                if key in project_annotations[project]:
                    label = TAG_LABELS.get(key, key.replace('_', ' ')).lower() + 's'
                    try:
                        value = annotation_counts[key].get(item.id, 0)
                    except KeyError:
                        value = 0
                    annotations[key] = {
                        'label': label,
                        'count': value,
                    }

            result[item] = {
                'is_bookmarked': item.id in bookmarks,
                'has_seen': seen_groups.get(item.id, active_date) > active_date,
                'annotations': annotations,
            }
        return result

    def serialize(self, obj, attrs, user):
        status = obj.get_status()
        if status == STATUS_RESOLVED:
            status_label = 'resolved'
        elif status == STATUS_MUTED:
            status_label = 'muted'
        else:
            status_label = 'unresolved'

        if obj.team:
            permalink = absolute_uri(reverse('sentry-group', args=[
                obj.team.slug, obj.project.slug, obj.id]))
        else:
            permalink = None

        d = {
            'id': str(obj.id),
            'count': str(obj.times_seen),
            'title': obj.message_short,
            'culprit': obj.culprit,
            'permalink': permalink,
            'firstSeen': obj.first_seen,
            'lastSeen': obj.last_seen,
            'timeSpent': obj.avg_time_spent,
            'canResolve': user.is_authenticated(),
            'status': {
                'id': status,
                'name': status_label,
            },
            'isResolved': obj.get_status() == STATUS_RESOLVED,
            'isPublic': obj.is_public,
            # 'score': getattr(obj, 'sort_value', 0),
            'project': {
                'name': obj.project.name,
                'slug': obj.project.slug,
            },
        }
        if hasattr(obj, 'is_bookmarked'):
            d['isBookmarked'] = obj.is_bookmarked
        if hasattr(obj, 'has_seen'):
            d['hasSeen'] = obj.has_seen
        if hasattr(obj, 'historical_data'):
            d['historicalData'] = obj.historical_data
        if hasattr(obj, 'annotations'):
            d['annotations'] = obj.annotations
        # if request:
        #     d['tags'] = list(get_tags(obj, request))
        return d
