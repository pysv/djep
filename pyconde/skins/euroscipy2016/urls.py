from django.conf.urls import include, url

urlpatterns = [
    url(r'^2016test/$', include('pyconde.urls')),
]
