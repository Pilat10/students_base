from django.conf.urls import patterns, url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('api.views',
    url(r'^group/$', views.GroupList.as_view(), name='group-list'),
    url(r'^group/(?P<pk>[0-9]+)/$', views.GroupDetail.as_view(),
        name='group-detail'),
    url(r'^studets/$', views.StudentList.as_view(), name='student-list'),
    url(r'^studets/(?P<pk>[0-9]+)/$', views.StudentDetail.as_view(),
        name='studets-detail'),
#    url(r'^snippets/$', views.SnippetList.as_view(), name='snippet-list'),
#    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(),
#        name='snippet-detail'),
#    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
#        views.SnippetHighlight.as_view(), name='snippet-highlight'),
#    url(r'^users/$', views.UserList.as_view(), name='user-list'),
#    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),
#        name='user-detail'),

)

urlpatterns = format_suffix_patterns(urlpatterns)