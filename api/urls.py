from django.conf.urls import patterns, url, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('api.views',
    url(r'^group/$', views.GroupList.as_view(), name='group-list'),
    url(r'^group/(?P<pk>[0-9]+)/$', views.GroupDetail.as_view(),
        name='group-detail'),
    url(r'^students/$', views.StudentList.as_view(), name='student-list'),
    url(r'^students/(?P<pk>[0-9]+)/$', views.StudentDetail.as_view(),
        name='studets-detail'),
    url(r'^docs/', include('rest_framework_swagger.urls')),

)

urlpatterns = format_suffix_patterns(urlpatterns)