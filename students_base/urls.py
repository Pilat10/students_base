from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

from base import views as base_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('api.urls', namespace='api')),
    path('ang/api-auth/', include('rest_framework.urls')),

    path('groups/', base_views.GroupList.as_view(), name='group_list'),
    path('groups/add/', base_views.GroupAdd.as_view(), name='group_add'),
    path('groups/edit/<int:group_id>/', base_views.GroupEdit.as_view(),
         name='group_edit'),
    path('groups/delete/<int:group_id>/', base_views.GroupDelete.as_view(),
         name='group_delete'),
    path('groups/<int:group_id>/', base_views.StudentList.as_view(),
         name='student_list'),

    path('student/add/', base_views.StudentAdd.as_view(), name='student_add'),
    path('student/edit/<int:student_id>/', base_views.StudentEdit.as_view(),
         name='student_edit'),
    path('student/delete/<int:student_id>/',
         base_views.StudentDelete.as_view(), name='student_delete'),

    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='login'),
    path('login_email/', auth_views.LoginView.as_view(
        template_name='registration/login_email.html'), name='login_email'),
    path('logout/', auth_views.LogoutView.as_view(next_page='group_list'),
         name='logout'),

    # AngularJS SPA shell (html5Mode). ensure_csrf_cookie because every DRF
    # APIView is csrf_exempt and index_angular.html has no {% csrf_token %},
    # so nothing would ever set the csrftoken cookie the SPA needs to send
    # as X-CSRFToken.
    re_path(r'^app/', ensure_csrf_cookie(
        TemplateView.as_view(template_name='index_angular.html'))),
]
