"""
sentry.runner.commands.migrate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2017 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, print_function

import click
from sentry.runner.decorators import configuration


def _get_install_id():
    from sentry import options
    install_id = options.get('sentry:install-id')
    if not install_id:
        from hashlib import sha1
        from uuid import uuid4
        install_id = sha1(uuid4().bytes).hexdigest()
        options.set('sentry:install-id', install_id)
    return install_id


def _get_api_token():
    from django.conf import settings
    click.echo()
    click.echo('Before we can get started, we need an API Token with the following scopes:')
    click.echo('- %s' % ', '.join(sorted(settings.SENTRY_SCOPES)))
    click.echo()
    return click.prompt('Enter API Token', hide_input=True)


def _get_events_30d():
    from datetime import timedelta
    from django.utils import timezone
    from sentry.app import tsdb
    end = timezone.now()
    return tsdb.get_sums(
        model=tsdb.models.internal,
        keys=['events.total'],
        start=end - timedelta(days=30),
        end=end,
    )['events.total']


def sort_dependencies(app_list):
    """
    Similar to Django's except that we discard the important of natural keys
    when sorting dependencies (i.e. it works without them).
    """
    from django.db.models import get_model, get_models

    # Process the list of models, and get the list of dependencies
    model_dependencies = []
    models = set()
    for app, model_list in app_list:
        if model_list is None:
            model_list = get_models(app)

        for model in model_list:
            models.add(model)
            # Add any explicitly defined dependencies
            if hasattr(model, 'natural_key'):
                deps = getattr(model.natural_key, 'dependencies', [])
                if deps:
                    deps = [get_model(*d.split('.')) for d in deps]
            else:
                deps = []

            # Now add a dependency for any FK relation with a model that
            # defines a natural key
            for field in model._meta.fields:
                if hasattr(field.rel, 'to'):
                    rel_model = field.rel.to
                    if rel_model != model:
                        deps.append(rel_model)

            # Also add a dependency for any simple M2M relation with a model
            # that defines a natural key.  M2M relations with explicit through
            # models don't count as dependencies.
            for field in model._meta.many_to_many:
                rel_model = field.rel.to
                if rel_model != model:
                    deps.append(rel_model)
            model_dependencies.append((model, deps))

    model_dependencies.reverse()
    # Now sort the models to ensure that dependencies are met. This
    # is done by repeatedly iterating over the input list of models.
    # If all the dependencies of a given model are in the final list,
    # that model is promoted to the end of the final list. This process
    # continues until the input list is empty, or we do a full iteration
    # over the input models without promoting a model to the final list.
    # If we do a full iteration without a promotion, that means there are
    # circular dependencies in the list.
    model_list = []
    while model_dependencies:
        skipped = []
        changed = False
        while model_dependencies:
            model, deps = model_dependencies.pop()

            # If all of the models in the dependency list are either already
            # on the final model list, or not on the original serialization list,
            # then we've found another model with all it's dependencies satisfied.
            found = True
            for candidate in ((d not in models or d in model_list) for d in deps):
                if not candidate:
                    found = False
            if found:
                model_list.append(model)
                changed = True
            else:
                skipped.append((model, deps))
        if not changed:
            raise RuntimeError("Can't resolve dependencies for %s in serialized app list." %
                ', '.join('%s.%s' % (model._meta.app_label, model._meta.object_name)
                for model, deps in sorted(skipped, key=lambda obj: obj[0].__name__))
            )
        model_dependencies = skipped

    return model_list


def Client(base_url, api_token):
    from requests import Session

    class SentryClient(Session):
        def __init__(self, base, token):
            super(SentryClient, self).__init__()
            self.base = base
            self.headers.update({
                'Authorization': 'Bearer %s' % token,
            })

        def request(self, method, url, **kwargs):
            return super(SentryClient, self).request(
                method=method,
                url=self.base + '/api/0' + url,
                **kwargs
            )

    return SentryClient(base_url, api_token)


@click.command()
@click.option('--organization', default=None, metavar='SLUG')
@click.option('--base-url', default='https://sentry.io')
@click.option('--api-token', default=None)
@configuration
def migrate(organization, base_url, api_token):
    "Migrate data to hosted Sentry account"
    from django.conf import settings
    from sentry.models import Organization

    if organization:
        organization = Organization.objects.get(slug=organization)

    if not organization:
        if not settings.SENTRY_SINGLE_ORGANIZATION:
            raise click.ClickException('Please supply an --organization slug to migrate')
        organization = Organization.get_default()

    base_url = base_url.rstrip('/')

    click.echo('You are about to migrate all of the data')
    click.echo('for the following organization over to a')
    click.echo('hosted Sentry account:')
    click.echo()
    click.echo('- %s (%s)' % (organization.name, organization.slug))
    click.echo()
    if not click.confirm('Would you like to continue?'):
        import sys
        sys.exit(0)

    if not api_token:
        api_token = _get_api_token()

    click.echo()
    click.echo('API Token: %s%s' % (api_token[:8], '*' * 12))

    install_id = _get_install_id()
    click.echo('Install ID: %s' % install_id)

    click.echo()

    events_30d = _get_events_30d()
    click.echo('Usage past 30 days: %d' % events_30d)
    click.echo('Estimated cost: $%d' % 0)

    client = Client(base_url, api_token)

    click.echo()
    click.echo('Verifying API Token... ', nl=False)
    rv = client.get('/')
    if rv.status_code != 200:
        raise click.ClickException(rv.text)
    click.echo('OK')

    click.echo('Fetching upstream organizations... ', nl=False)
    organizations = client.get('/organizations/').json()
    click.echo('%d' % len(organizations))

    if len(organizations) == 0:
        raise click.ClickException('You have no organizations to migrate into. Please create one and try again.')

    if len(organizations) == 1:
        to_org = organizations[0]
        click.echo('> Assuming organization: %s (%s)' % (to_org['name'], to_org['slug']))
    else:
        click.echo()
        for org in organizations:
            click.echo('- %s (%s)' % (org['name'], org['slug']))
        click.echo()
        org_slug = click.prompt('Enter slug:')
        for org in organizations:
            if org['slug'] == org_slug:
                to_org = org
                break

    from django.db.models import get_apps
    from django.core import serializers
    from sentry.models import Project

    projects = list(Project.objects.filter(organization=organization))
    project_ids = {p.id for p in projects}

    def yield_objects():
        app_list = [(a, None) for a in get_apps()]

        yield organization

        for project in projects:
            yield project

        # Collate the objects to be serialized.
        for model in sort_dependencies(app_list):
            if (
                not getattr(model, '__core__', True) or
                model.__name__.lower() in ('organization', 'project') or
                model._meta.proxy
            ):
                continue

            fields = set(model._meta.get_all_field_names())
            filters = {}
            if 'organization' in fields:
                filters['organization'] = organization.id
            if 'organization_id' in fields:
                filters['organization_id'] = organization.id
            if 'project' in fields:
                filters['project__in'] = project_ids
            if 'project_id' in fields:
                filters['project_id__in'] = project_ids
            if not filters:
                continue
            queryset = model._base_manager.order_by(model._meta.pk.name)
            for obj in queryset.filter(**filters).iterator():
                click.echo('.', nl=False)
                yield obj

    from six import BytesIO

    click.echo('Generating export', nl=False)
    dest = BytesIO()
    serializers.serialize("json", yield_objects(), stream=dest,
                          use_natural_keys=True)

    dest.seek(0)

    click.echo()
    click.echo('Uploading...', nl=False)
    rv = client.post('/migrations/%s/%s/' % (to_org['slug'], install_id), files=[
        ('export', ('export.json', dest, 'application/json')),
    ])
    click.echo(' %d' % rv.status_code)
    click.echo()
    click.echo('# import log')
    for log in rv.json()['log']:
        click.echo(log)
