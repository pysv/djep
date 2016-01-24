# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Fieldset, Field, HTML

from ..conference.models import current_conference
from ..forms import Submit

from . import validators
from .utils import get_full_name, SEND_MAIL_CHOICES


NUM_ACCOMPANYING_CHILDREN_CHOICES = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return get_full_name(obj)


class SignUpForm(auth_forms.UserCreationForm):
    """
    Override for the default registration form - adds new fields:

    * Avatar for allowing the user to upload a profile picture
    * and short_info, which allows the user to introduce herself to the
      other attendees/speakers.
    * Organisation name
    * Twitter handle
    * website (URL)
    * Number of accompanying children (dropdown selection)
    * Info about children's ages (free text)

    All these fields are publicly accessible and optional.
    """

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        account_fields = Fieldset(
            _('Login information'),
            Field('username', autofocus="autofocus"),
            'email',
            'password',
            'password_repeat'
        )
        profile_fields = Fieldset(
            _('Personal information'),
            'full_name',
            'display_name',
            'addressed_as',
            'avatar',
            'short_info'
        )
        profession_fields = Fieldset(
            _('Professional information'),
            'organisation',
            'twitter',
            'website',
            Field('tags', css_class='tags-input'),
            'accept_job_offers'
        )
        privacy_fields = Fieldset(
            _('Privacy Policy'),
            HTML(_('{% load cms_tags %}<p class="control-group">Due to data protection '
                   'regulations you need to explicitly accept our '
                   '<a href="{% page_url "privacy-policy" %}">privacy policy</a>.</p>')),
            'accept_privacy_policy',
            'accept_pysv_conferences',
            'accept_ep_conferences'
        )
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            account_fields,
            profile_fields,
            profession_fields,
            privacy_fields,
            ButtonHolder(Submit('submit', _('Create account'), css_class='btn btn-primary'))
        )
        if settings.ACCOUNTS_FALLBACK_TO_GRAVATAR:
            self.fields['avatar'].help_text = _("""Please upload an image with a side length of at least 300 pixels.<br />If you don't upload an avatar your Gravatar will be used instead.""")

    def clean_twitter(self):
        """
        Allow the user to enter either "@foo" or "foo" as their twitter handle.
        """
        value = self.cleaned_data.get('twitter', '')
        value = value.lstrip('@')
        validators.twitter_username(value)  # validates the max_length
        return value


class ReviewerApplicationForm(forms.Form):

    class Meta:
        fields = ()

    def __init__(self, *args, **kwargs):
        super(ReviewerApplicationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'apply',
            ButtonHolder(Submit('save', _("Apply now!"), css_class='btn btn-success')))


class SendMailForm(forms.Form):

    target = forms.ChoiceField(choices=SEND_MAIL_CHOICES,
        label=_('Send mail to'))
    subject = forms.CharField(label=_('Subject'))
    text = forms.CharField(label=_('Message'), widget=forms.Textarea,
        help_text=_('The text may contain the following placeholders:<ul>'
                    '<li><code>$$RECEIVER$$</code></li>'
                    '<li><code>$$CONFERENCE$$</code></li>'
                    '<li><code>$$DOMAIN$$</code></li>'
                    '</ul>'))

    def __init__(self, *args, **kwargs):
        super(SendMailForm, self).__init__(*args, **kwargs)
        self.fields['subject'].help_text = _('The subject will be prefixed by '
                                             '<code>[%(prefix)s] </code>') % {
            'prefix': current_conference(),
        }
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'target',
            'subject',
            'text',
            ButtonHolder(Submit('submit', _('Send mail'), css_class='btn btn-primary'))
        )
