from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('pyconde.accounts.views',
    url(r'^logout/$', 'logout', name='auth_logout'),
    url(r'^ajax/users$', views.AutocompleteUser.as_view()),
    url(r'^ajax/tags/$', views.AutocompleteTags.as_view(), name='ajax-tags'),
    url(r'^profile/(?P<uid>\d+)/$', views.ProfileView.as_view(),
        name='account_profile'),
    url(r'^profile/reviewer/apply/$', views.ReviewerApplication.as_view(),
        name='reviewer_application'),
    url(r'^sendmail/$', 'sendmail_view', name='account_sendmail'),
    url(r'^sendmail/done/$', 'sendmaildone_view', name='account_sendmail_done'),
)
