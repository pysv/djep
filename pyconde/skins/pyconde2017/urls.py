from django.conf.urls import include, url

urlpatterns = [
    url(r'^2017test/$', include('pyconde.urls')),
]
