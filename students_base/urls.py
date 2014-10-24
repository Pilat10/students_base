from django.conf.urls import patterns, include, url
from base.views import *
from django.contrib import admin
from api import urls as api_urls
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(api_urls, namespace='api')),
    url(r'^groups/$', GroupList.as_view(), name='group_list'),
    url(r'^groups/(?P<group_id>\d+)/$', StudentList.as_view(),
        name='student_list'),
    url(r'^groups/add/$', GroupAdd.as_view(), name='group_add'),
    url(r'^groups/edit/(?P<group_id>\d+)/$', GroupEdit.as_view(),
        name='group_edit'),
    url(r'^groups/delete/(?P<group_id>\d+)/$', GroupDelete.as_view(),
        name='group_delete'),

    url(r'^student/add/$', StudentAdd.as_view(), name='student_add'),
    url(r'^student/edit/(?P<student_id>\d+)/$', StudentEdit.as_view(),
        name='student_edit'),
    url(r'^student/delete/(?P<student_id>\d+)/$', StudentDelete.as_view(),
        name='student_delete'),

    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'registration/login.html',
         'redirect_field_name': 'groups/'}, name='login'),
    url(r'^login_email/$', 'django.contrib.auth.views.login',
        {'template_name': 'registration/login_email.html',
         'redirect_field_name': 'groups/'}, name='login_email'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': 'group_list'}, name='logout'),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

)
