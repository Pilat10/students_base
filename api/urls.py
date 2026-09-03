from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api import views

app_name = 'api'

urlpatterns = [
    path('department/', views.DepartmentListView.as_view(),
         name='department-list'),
    path('department/<int:pk>/', views.DepartmentDetailView.as_view(),
         name='department-detail'),
    path('group/', views.GroupListView.as_view(), name='group-list'),
    path('group/<int:pk>/', views.GroupDetailView.as_view(),
         name='group-detail'),
    path('student/', views.StudentListView.as_view(), name='student-list'),
    path('student/export/', views.StudentExportView.as_view(),
         name='student-export'),
    path('student/<int:pk>/', views.StudentDetailView.as_view(),
         name='student-detail'),

    path('auth/', views.LoginView.as_view(), name='auth'),
    path('auth-token/', views.LoginTokenView.as_view(), name='auth-token'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'),
         name='docs'),
]
