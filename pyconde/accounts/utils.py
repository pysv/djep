# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


def get_display_name(user):
    """
    Tries to return (in order):

        * ``user.display_name``
        * ``user.username``
    """
    if user is None:
        return None
    return user.get_display_name()


def get_full_name(user):
    """
    Tries to return (in order):

        * ``user.full_name``
        * ``user.display_name``
        * ``user.username``
    """
    if user is None:
        return None
    return user.get_full_name(user)


def get_addressed_as(user):
    """
    Tries to return (in order):

        * ``user.addressed_as``
        * ``user.display_name``
        * ``user.username``
    """
    if user is None:
        return None
    if user.addressed_as:
        return user.addressed_as
    return user.get_display_name()


_valid_purchase = ('invoice_created', 'payment_received')

_SEND_MAIL_MAP = (
    ('', _('Please select the target group'), None),
    (
        'all',
        _('All registered users'),
        lambda qs: qs
    ),
    (
        'buyers',
        _('All users having valid purchases'),
        lambda qs: qs.filter(purchase__state__in=_valid_purchase)
                     .distinct()
    ),
    (
        'ticket_holder',
        _('All users having at least one ticket directly assigned'),
        lambda qs: qs.filter(attendees_ticket_tickets__isnull=False,
                             attendees_ticket_tickets__purchase__state__in=_valid_purchase)
                     .distinct()
    ),
)

SEND_MAIL_CHOICES = tuple((i[0], i[1]) for i in _SEND_MAIL_MAP)
SEND_MAIL_FILTERS = {i[0]: i[2] for i in _SEND_MAIL_MAP}
