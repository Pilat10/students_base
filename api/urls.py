from django.conf.urls import patterns, url, include
from api import views

urlpatterns = patterns('api.views',
    url(r'^department/$', views.DepartmentListView.as_view(),
        name='department-list'),
    url(r'^department/(?P<pk>[0-9]+)/$', views.DepartmentDetailView.as_view(),
        name='department-detail'),
    url(r'^group/$', views.GroupListView.as_view(), name='group-list'),
    url(r'^group/(?P<pk>[0-9]+)/$', views.GroupDetailView.as_view(),
        name='group-detail'),
    url(r'^student/$', views.StudentListView.as_view(), name='student-list'),
    url(r'^student/(?P<pk>[0-9]+)/$', views.StudentDetailView.as_view(),
        name='studets-detail'),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^auth/', views.LoginView.as_view(), name="auth"),
    url(r'^auth-token/', views.LoginTokenView.as_view(), name="auth"),
)
