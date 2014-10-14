"""
Api urls module
"""
from django.conf.urls import patterns, url
from api import views as api_views

urlpatterns = patterns('',
    url(r'^$', api_views.ApiRootView.as_view(), name='api_root'),
)
