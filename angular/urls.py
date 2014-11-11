from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^.*$', TemplateView.as_view(
        template_name='index_angular.html')),

    #url(r'^groups/$', TemplateView.as_view(
    #    template_name='angular/group_list.html'), name='group-list'),
    #url(r'^groups/(?P<group_id>\d+)/$', TemplateView.as_view(
    #    template_name='angular/student_list.html'), name='student_list'),
    #url(r'^groups/add/$', GroupAdd.as_view(), name='group_add'),
    #url(r'^groups/edit/(?P<group_id>\d+)/$', GroupEdit.as_view(),
    #    name='group_edit'),
    #url(r'^groups/delete/(?P<group_id>\d+)/$', GroupDelete.as_view(),
    #    name='group_delete'),

    #url(r'^student/add/$', StudentAdd.as_view(), name='student_add'),
    #url(r'^student/edit/(?P<student_id>\d+)/$', StudentEdit.as_view(),
    #    name='student_edit'),
    #url(r'^student/delete/(?P<student_id>\d+)/$', StudentDelete.as_view(),
    #    name='student_delete'),
    )