from __future__ import absolute_import

from django.db import IntegrityError, transaction

from rest_framework.response import Response

from .project_releases import ReleaseSerializer
from sentry.api.base import DocSection
from sentry.api.bases.organization import OrganizationEndpoint, OrganizationReleasePermission
from sentry.api.paginator import OffsetPaginator
from sentry.api.serializers import serialize
from sentry.api.serializers.rest_framework import ListField
from sentry.models import Project, Release
from sentry.plugins.interfaces.releasehook import ReleaseHook


class ReleaseSerializerWithProjects(ReleaseSerializer):
    projects = ListField()


class OrganizationReleasesEndpoint(OrganizationEndpoint):
    doc_section = DocSection.RELEASES
    permission_classes = (OrganizationReleasePermission,)

    def get(self, request, organization):
        """
        List an Organizations Releases
        ``````````````````````````````

        Return a list of releases for a given organization.

        :pparam string organization_slug: the organization short name

        :qparam string query: this parameter can be used to create a
                              "starts with" filter for the version.
        """
        query = request.GET.get('query')

        queryset = Release.objects.filter(
            organization=organization,
        ).select_related('owner')

        if query:
            queryset = queryset.filter(
                version__istartswith=query,
            )

        queryset = queryset.extra(select={
            'sort': 'COALESCE(date_released, date_added)',
        })

        return self.paginate(
            request=request,
            queryset=queryset,
            order_by='-sort',
            paginator_cls=OffsetPaginator,
            on_results=lambda x: serialize(x, request.user),
        )

    def post(self, request, organization):
        """
        Create a New Release
        ````````````````````

        Create a new release for the given Organization.  Releases are used by
        Sentry to improve it's error reporting abilities by correlating
        first seen events with the release that might have introduced the
        problem.

        Releases are also necessary for sourcemaps and other debug features
        that require manual upload for functioning well.

        :pparam string organization_slug: the slug of the organization the
                                          release belongs to.
        :param string version: a version identifier for this release.  Can
                               be a version number, a commit hash etc.
        :param string ref: an optional commit reference.  This is useful if
                           a tagged version has been provided.
        :param url url: a URL that points to the release.  This can be the
                        path to an online interface to the sourcecode
                        for instance.
        :param array projects: a list of project slugs that are involved in
                               this release
        :param datetime dateStarted: an optional date that indicates when the
                                     release process started.
        :param datetime dateReleased: an optional date that indicates when
                                      the release went live.  If not provided
                                      the current time is assumed.
        :auth: required
        """
        serializer = ReleaseSerializer(data=request.DATA)

        if serializer.is_valid():
            result = serializer.object

            projects = Project.object.filter(organization=organization,
                                             slug__in=result.projects)
            invalid_projects = list(set(result.projects) - {p.slug for p in projects})
            if invalid_projects:
                # TODO: make sure the error format matches serializer errors
                return Response({'projects': 'Invalid project slugs'}, status=400)

            try:
                with transaction.atomic():
                    # release creation is idempotent to simplify user
                    # experiences
                    release, created = Release.objects.create(
                        # TODO(jess): deal with this
                        project=projects[0],
                        organization=organization,
                        version=result['version'],
                        ref=result.get('ref'),
                        url=result.get('url'),
                        owner=result.get('owner'),
                        date_started=result.get('dateStarted'),
                        date_released=result.get('dateReleased'),
                    ), True
            except IntegrityError:
                release, created = Release.objects.get(
                    organization=organization,
                    version=result['version'],
                ), False
                # was_released = bool(release.date_released)
            # else:
                # was_released = False

            for p in projects:
                release.add_project(p)

            commit_list = result.get('commits')
            if commit_list:
                hook = ReleaseHook(organization)
                # TODO(dcramer): handle errors with release payloads
                hook.set_commits(release.version, commit_list)

            # TODO(jess): activity is linked to a project
            # if not was_released and release.date_released:
            #     activity = Activity.objects.create(
            #         type=Activity.RELEASE,
            #         project=project,
            #         ident=result['version'],
            #         data={'version': result['version']},
            #         datetime=release.date_released,
            #     )
            #     activity.send_notification()

            if not created:
                # This is the closest status code that makes sense, and we want
                # a unique 2xx response code so people can understand when
                # behavior differs.
                #   208 Already Reported (WebDAV; RFC 5842)
                status = 208
            else:
                status = 201

            return Response(serialize(release, request.user), status=status)
        return Response(serializer.errors, status=400)
