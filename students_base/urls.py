from django.conf.urls import patterns, include, url
from base.views import *
from django.contrib import admin
admin.autodiscover()

test = True

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'students_base.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),



    url(r'^admin/', include(admin.site.urls)),
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

)
