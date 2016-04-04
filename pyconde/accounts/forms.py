# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Fieldset, Field, HTML, Div

from ..conference.models import current_conference
from ..forms import Submit

from . import validators, models
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
        self.fields['password1'] = forms.CharField(
            label=_("Password"),
            widget=forms.PasswordInput()
        )
        self.fields['password2'] = forms.CharField(
            label=_("Password (again)"),
            widget=forms.PasswordInput(),
            help_text=_('Please repeat your password.'),
        )
        account_fields = Fieldset(
            _('Login information'),
            Div(Field('username', autofocus="autofocus"), css_class="col-md-12"),
            Div('email', css_class="col-md-12"),
            Div('password1', css_class="col-md-12"),
            Div('password2', css_class="col-md-12"),
            css_class="row"
        )
        profile_fields = Fieldset(
            _('Personal information'),
            Div('first_name', css_class="col-md-12"),
            Div('last_name', css_class="col-md-12"),
            Div('short_info', css_class="col-md-12"),
            Div('avatar', css_class="col-md-12"),
            Div('display_name', css_class="col-md-12"),
            Div('addressed_as', css_class="col-md-12"),
            Div('num_accompanying_children', css_class="col-md-12"),
            Div('age_accompanying_children', css_class="col-md-12"),
            css_class="row"
        )
        profession_fields = Fieldset(
            _('Professional information'),
            Div('organisation', css_class="col-md-12"),
            Div('twitter', css_class="col-md-12"),
            Div('website', css_class="col-md-12"),
            Div(Field('tags', css_class='tags-input'), css_class="col-md-12"),
            Div('accept_job_offers', css_class="col-md-12"),
            css_class="row"
        )
        privacy_fields = Fieldset(
            _('Privacy Policy'),
            #HTML(_('{% load cms_tags %}<p class="control-group">Due to data protection '
            #       'regulations you need to explicitly accept our '
            #       '<a href="{% page_url "privacy-policy" %}">privacy policy</a>.</p>')),
            Div('accept_privacy_policy', css_class="col-md-12"),
            css_class="row"
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

    class Meta:
        model = models.User
        fields = ('username', 'email', 'first_name', 'last_name', 'short_info', 'avatar',
            'num_accompanying_children', 'age_accompanying_children', 'twitter', 'website',
            'organisation', 'display_name', 'addressed_as', 'accept_job_offers', 'tags')


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
