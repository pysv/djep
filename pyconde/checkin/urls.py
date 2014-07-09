# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, patterns


urlpatterns = patterns(
    'pyconde.checkin.views',
    url(r'^purchase/$', 'purchase_view',
        name='checkin_purchase'),
    url(r'^purchase/(?P<pk>\d+)/$', 'purchase_detail_view',
        name='checkin_purchase_detail'),
    url(r'^search/$', 'search_view',
        name='checkin_search'),
)
