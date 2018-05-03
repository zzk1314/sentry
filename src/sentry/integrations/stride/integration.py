from __future__ import absolute_import

from sentry.identity.pipeline import IdentityProviderPipeline
from sentry.integrations import Integration, IntegrationMetadata
from sentry.pipeline import NestedPipelineView
from sentry.utils.http import absolute_uri


alert_link = {
    'text': 'Visit the **Atlassian Marketplace** to install this integration.',
    # TODO(jess): update this when we have our app listed on the
    # atlassian marketplace
    'link': 'https://marketplace.atlassian.com/',
}


metadata = IntegrationMetadata(
    description='Integrate Sentry with Stride.',
    author='The Sentry Team',
    issue_url='https://github.com/getsentry/sentry/issues/new?title=Stride%20Integration:%20&labels=Component%3A%20Integrations',
    source_url='https://github.com/getsentry/sentry/tree/master/src/sentry/integrations/stride',
    aspects={
        'alert_link': alert_link,
    },
)


class StrideIntegration(Integration):
    key = 'stride'
    name = 'Stride'
    metadata = metadata

    can_add = False

    # identity_oauth_scopes = frozenset([
    #     'participate:conversation',
    # ])

    # setup_dialog_config = {
    #     'width': 600,
    #     'height': 900,
    # }

    # def get_pipeline_views(self):
    #     identity_pipeline_config = {
    #         'oauth_scopes': self.identity_oauth_scopes,
    #         'redirect_url': absolute_uri('/extensions/stride/setup/'),
    #     }

    #     identity_pipeline_view = NestedPipelineView(
    #         bind_key='identity',
    #         provider_key='stride',
    #         pipeline_cls=IdentityProviderPipeline,
    #         config=identity_pipeline_config,
    #     )

    #     return [identity_pipeline_view]

    # def build_integration(self, state):
    #     data = state['identity']['data']
    #     assert data['ok']

    #     scopes = sorted(self.identity_oauth_scopes)
    #     team_data = self.get_team_info(data['access_token'])

    #     return {
    #         'name': data['team_name'],
    #         'external_id': data['team_id'],
    #         'metadata': {
    #             'access_token': data['access_token'],
    #             'scopes': scopes,
    #             'icon': team_data['icon']['image_132'],
    #             'domain_name': team_data['domain'] + '.slack.com',
    #         },
    #         'user_identity': {
    #             'type': 'slack',
    #             'external_id': data['authorizing_user_id'],
    #             'scopes': [],
    #             'data': {},
    #         },
    #     }
