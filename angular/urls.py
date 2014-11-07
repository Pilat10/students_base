from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^group/$', TemplateView.as_view(
        template_name='angular/group_list.html'), name='group-list'),
    )