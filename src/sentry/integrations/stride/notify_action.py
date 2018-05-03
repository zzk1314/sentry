from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _

from sentry import http
from sentry.rules.actions.base import EventAction
from sentry.utils import metrics
from sentry.models import Integration

ENDPOINT = 'https://api.atlassian.com/site/{cloud_id}/conversation/{conversation_id}/message'


class StrideNotifyServiceForm(forms.Form):
    site = forms.ChoiceField(choices=(), widget=forms.Select())
    conversation = forms.CharField(widget=forms.TextInput())
    conversation_id = forms.HiddenInput()
    tags = forms.CharField(required=False, widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        # NOTE: Workspace maps directly to the integration ID
        site_list = [(i.id, i.name) for i in kwargs.pop('integrations')]
        self.conversation_transformer = kwargs.pop('conversation_transformer')

        super(StrideNotifyServiceForm, self).__init__(*args, **kwargs)

        if site_list:
            self.fields['site'].initial = site_list[0][0]

        self.fields['site'].choices = site_list
        self.fields['site'].widget.choices = self.fields['site'].choices

    def clean(self):
        cleaned_data = super(StrideNotifyServiceForm, self).clean()

        site = cleaned_data.get('site')
        conversation = cleaned_data.get('conversation', '')

        conversation_id = self.conversation_transformer(site, conversation)

        if conversation_id is None and site is not None:
            params = {
                'conversation': conversation,
                'site': dict(self.fields['site'].choices).get(int(site)),
            }

            raise forms.ValidationError(
                _('The Stride conversation "%(conversation)s" does not exist or has not been granted access for the Stride %(site)s site.'),
                code='invalid',
                params=params,
            )

        cleaned_data['conversation'] = conversation
        cleaned_data['conversation_id'] = conversation_id

        return cleaned_data


class StrideNotifyServiceAction(EventAction):
    form_cls = StrideNotifyServiceForm
    label = u'Send a notification to the {site} Stride site to {conversation} and show tags {tags} in notification'

    def __init__(self, *args, **kwargs):
        super(StrideNotifyServiceAction, self).__init__(*args, **kwargs)
        self.form_fields = {
            'site': {
                'type': 'choice',
                'choices': [(i.id, i.name) for i in self.get_integrations()]
            },
            'conversation': {
                'type': 'string',
                'placeholder': 'i.e Alerts'
            },
            'tags': {
                'type': 'string',
                'placeholder': 'i.e environment,user,my_tag'
            }
        }

    def is_enabled(self):
        return self.get_integrations().exists()

    def after(self, event, state):
        if event.group.is_ignored():
            return

        integration_id = self.get_option('site')
        conversation_id = self.get_option('conversation_id')
        # tags = set(self.get_tags_list())

        try:
            integration = Integration.objects.get(
                provider='stride',
                organizations=self.project.organization,
                id=integration_id
            )
        except Integration.DoesNotExist:
            # Integration removed, rule still active.
            return

        def send_notification(event, futures):
            payload = {
                'body': {
                    'version': 1,
                    'type': 'doc',
                    'content': [{
                        'type': 'paragraph',
                        'content': [{
                            'type': 'text',
                            'text': 'Hello world',
                        }]
                    }]
                }
            }

            session = http.build_session()
            resp = session.post(ENDPOINT.format(
                cloud_id=integration.metadata['cloud_id'],
                conversation_id=conversation_id,
            ), json=payload, headers={
                'Authorization': 'Bearer {}'.format(integration.metadata['token'])
            })
            resp.raise_for_status()
            resp = resp.json()
            if not resp.get('ok'):
                self.logger.info('rule.fail.stride_post', extra={'error': resp.get('error')})

        key = u'stride:{}:{}'.format(integration_id, conversation_id)

        metrics.incr('notifications.sent', instance='stride.notification')
        yield self.future(send_notification, key=key)

    def render_label(self):
        try:
            integration_name = Integration.objects.get(
                provider='stride',
                organizations=self.project.organization,
                id=self.get_option('site')
            ).name
        except Integration.DoesNotExist:
            integration_name = '[removed]'

        tags = self.get_tags_list()

        return self.label.format(
            workspace=integration_name,
            conversation=self.get_option('conversation'),
            tags=u'[{}]'.format(', '.join(tags)),
        )

    def get_tags_list(self):
        return [s.strip() for s in self.get_option('tags', '').split(',')]

    def get_integrations(self):
        return Integration.objects.filter(
            provider='stride',
            organizations=self.project.organization,
        )

    def get_form_instance(self):
        return self.form_cls(
            self.data,
            integrations=self.get_integrations(),
            conversation_transformer=self.get_conversation_id,
        )

    def get_conversation_id(self, integration_id, name):
        try:
            integration = Integration.objects.get(
                provider='stride',
                organizations=self.project.organization,
                id=integration_id,
            )
        except Integration.DoesNotExist:
            return None

        raise NotImplementedError
