# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.signals import user_logged_in
from markup_deprecated.templatetags.markup import markdown
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db import models
from django.db.models import Q

#from cms.models import CMSPlugin

from easy_thumbnails.fields import ThumbnailerImageField
from taggit.managers import TaggableManager

from . import validators
from .managers import UserManager


avatar_min_max_dimension = {}
if validators.AVATAR_MIN_DIMENSION:
    avatar_min_max_dimension.update({
        'min_w': validators.AVATAR_MIN_DIMENSION[0],
        'min_h': validators.AVATAR_MIN_DIMENSION[1]
    })
    if validators.AVATAR_MAX_DIMENSION:
        avatar_help_text = _('Please upload an image with a side length between %(min_w)dx%(min_h)d px and %(max_w)dx%(max_h)d px.')
        avatar_min_max_dimension.update({
            'max_w': validators.AVATAR_MAX_DIMENSION[0],
            'max_h': validators.AVATAR_MAX_DIMENSION[1]
        })
    else:
        avatar_help_text = _('Please upload an image with a side length of at least %(min_w)dx%(min_h)d px.')
else:
    if validators.AVATAR_MAX_DIMENSION:
        avatar_help_text = _('Please upload an image with a side length of at most %(max_w)dx%(max_h)d px.')
        avatar_min_max_dimension.update({
            'max_w': validators.AVATAR_MAX_DIMENSION[0],
            'max_h': validators.AVATAR_MAX_DIMENSION[1]
        })
    else:
        avatar_help_text = ''
avatar_help_text = avatar_help_text % avatar_min_max_dimension


class BadgeStatus(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    slug = models.SlugField(_('slug'), max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')

    def __unicode__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("Username"), max_length=256, unique=True)
    email = models.EmailField(_("E-Mail"), unique=True)
    first_name = models.CharField(_("First name"), max_length=30)
    last_name = models.CharField(_("Last name"), max_length=30)
    is_staff = models.BooleanField(_("Staff status"), default=False,
        help_text=_("Designates whether the user can log into this admin site."))
    is_active = models.BooleanField(_("Active"), default=True,
        help_text=_("Designates whether this user should be treated as active."
                    " Unselect this instead of deleting accounts."))
    date_joined = models.DateTimeField(_("Date joined"), default=timezone.now)

    short_info = models.TextField(_('short info'), blank=True)
    avatar = ThumbnailerImageField(
        _('avatar'), upload_to='avatars', null=True, blank=True,
        help_text=avatar_help_text,
        validators=[validators.avatar_dimension, validators.avatar_format]
    )
    num_accompanying_children = models.PositiveIntegerField(
        _('Number of accompanying children'), null=True, blank=True, default=0)
    age_accompanying_children = models.CharField(_("Age of accompanying children"),
        blank=True, max_length=20)
    twitter = models.CharField(_("Twitter"), blank=True, max_length=20,
        validators=[validators.twitter_username])
    website = models.URLField(_("Website"), blank=True)
    organisation = models.TextField(_('Organisation'), blank=True)
    full_name = models.CharField(_("Full name"), max_length=255, blank=True)
    display_name = models.CharField(_("Display name"), max_length=255,
        help_text=_('What name should be displayed to other people?'),
        blank=True)
    addressed_as = models.CharField(_("Address me as"), max_length=255,
        help_text=_('How should we call you in mails and dialogs throughout the website?'),
        blank=True)
    accept_pysv_conferences = models.BooleanField(_('Allow copying to PySV conferences'),
        default=False, blank=True)
    accept_ep_conferences = models.BooleanField(_('Allow copying to EPS conferences'),
        default=False, blank=True)
    accept_job_offers = models.BooleanField(_('Allow sponsors to send job offers'),
        default=False, blank=True)

    badge_status = models.ManyToManyField('accounts.BadgeStatus', blank=True,
        verbose_name=_('Badge status'), related_name='profiles')

    sessions_attending = models.ManyToManyField('schedule.Session', blank=True,
        related_name='attendees', verbose_name=_('Trainings'),
        limit_choices_to=Q(kind__slug__in=settings.SCHEDULE_ATTENDING_POSSIBLE))

    tags = TaggableManager(blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ['last_name', 'first_name', 'email']
        permissions = (
            ('send_user_mails', _('Allow sending mails to users through the website')),
            ('export_guidebook', _('Allow export of guidebook data')),
            ('see_checkin_info', _('Allow seeing check-in information')),
            ('perform_purchase', _('Allow performing purchases'))
        )

    @cached_property
    def short_info_rendered(self):
        return markdown(self.short_info, 'safe')

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        """Return either the full name or email if no name has been set."""
        full_name = self.email
        if self.first_name and self.last_name:
            full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name

    def get_short_name(self):
        """Return either the shortened full name or email if no name has been set."""
        short_name = self.email
        if self.first_name and self.last_name:
            short_name = '{}. {}'.format(self.first_name[0], self.last_name)
        return short_name

    def signup(self, first_name, last_name, commit=True):
        """Update the fields required for sign-up and accept the terms and conditions."""
        self.first_name = first_name
        self.last_name = last_name
        if commit:
            self.save()


#class UserListPlugin(CMSPlugin):
#
#    badge_status = models.ManyToManyField('BadgeStatus', blank=True,
#        verbose_name=_('Status'))
#    additional_names = models.TextField(_('Additional names'), blank=True,
#        default='', help_text=_('Users without account. One name per line.'))
#
#    def copy_relations(self, oldinstance):
#        self.badge_status = oldinstance.badge_status.all()
#
#    @property
#    def additional_names_list(self):
#        return list(set(bs for bs in self.additional_names.split('\n') if bs))
#

@receiver(user_logged_in)
def show_logged_in_message(request, user, **kwargs):
    messages.success(request, _("You've logged in successfully."),
                     fail_silently=True)
