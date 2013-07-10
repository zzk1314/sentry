"""
sentry.tasks.deletion
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2013 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from collections import defaultdict
from celery.task import task

"""
1. Collect all relations (fields, ordered)
2. Set a cursor per relation (only on the current relation)
3. Step through each relation, using chunking techniques to collect
   related objects
4. Repeat
"""

def collect_dependencies(model):
    dep_map = defaultdict(set)
    for related in model._meta.get_all_related_objects(
            include_hidden=True, include_proxy_eq=True):
        # field = related.field
        # if field.rel.on_delete == DO_NOTHING:
        #     continue
        if model == related.model:
            continue
        dep_map[model].add(related.model)
        for source, deps in collect_dependencies(related.model).iteritems():
            dep_map[source] |= deps

    for relation in model._meta.many_to_many:
        if not relation.rel.through:
            dep_map[model].add(related.rel.to)
            for source, deps in collect_dependencies(related.rel.to).iteritems():
                dep_map[source] |= deps

    return dep_map


def sort_dependencies(dependency_map):
    sorted_models = []
    while len(dependency_map) != len(sorted_models):
        for model, dep_set in dependency_map.iteritems():
            if not (d in sorted_models for d in dep_set):
                continue
            sorted_models.append(model)
    return sorted_models


def get_model_label(model):
    return (model._meta.app_label, model._meta.module_name)


@task(name='sentry.tasks.deletion.delete_object', queue='cleanup')
def delete_object(model_path, object_id, chunk_size=1000, cursor=None, _dependency_graph=None, **kwargs):
    from django.db.models import get_model
    from sentry.utils.imports import import_string

    log = delete_object.get_logger()

    model = import_string(model_path)

    if _dependency_graph is None:
        _dependency_graph = sort_dependencies(collect_dependencies(model))

    print _dependency_graph

    if cursor is None:
        cursor = (0,)

    dep_index, = cursor

    rel_meta_name, rel_name = _dependency_graph[dep_index]
    rel_model = get_model(*rel_meta_name)

    # TODO: dont use objects manager
    qs = rel_model.objects.filter(**{
        rel_name: object_id
    })

    has_objects = False
    for obj in qs[:chunk_size]:
        has_objects = True
        log.info("Removing %r", obj)
        obj.delete()

    if not has_objects:
        if dep_index < len(_dependency_graph):
            dep_index += 1
        else:
            log.info("Removing primary object %r = %r", model, object_id)
            model.objects.filter(pk=object_id).delete()
            return

    cursor = (dep_index,)
    delete_object.apply_async(
        kwargs={
            'model_path': model_path,
            'object_id': object_id,
            'chunk_size': chunk_size,
            'cursor': cursor,
            '_dependancy_map': _dependancy_map,
        },
    )
